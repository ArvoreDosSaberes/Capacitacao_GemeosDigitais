#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import { ChromaClient } from 'chromadb';
import Database from 'sqlite3';
import { config } from 'dotenv';

// Carregar configuração
config();

const DATA_DIR = process.env.DATA_DIR || '../.data';
const CHROMA_PATH = process.env.CHROMA_DB_PATH || `${DATA_DIR}/chroma_db`;
const SQLITE_PATH = process.env.SQLITE_DB_PATH || `${DATA_DIR}/documents.db`;
const OLLAMA_HOST = process.env.OLLAMA_HOST || 'http://localhost:11434';
const EMBEDDING_MODEL = process.env.OLLAMA_MODEL || 'mxbai-embed-large';

class RAGMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'rag-mcp-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.chromaClient = null;
    this.db = null;
    this.setupErrorHandling();
  }

  setupErrorHandling() {
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.cleanup();
      process.exit(0);
    });
  }

  async cleanup() {
    if (this.db) {
      await new Promise((resolve) => this.db.close(resolve));
    }
  }

  async initializeDatabases() {
    try {
      // Inicializar ChromaDB
      this.chromaClient = new ChromaClient({
        path: CHROMA_PATH
      });
      
      // Testar conexão com ChromaDB
      const collections = await this.chromaClient.listCollections();
      console.log(`[MCP] ChromaDB conectado. Coleções: ${collections.length}`);

      // Inicializar SQLite
      this.db = new Database(SQLITE_PATH);
      
      // Testar conexão com SQLite
      await new Promise((resolve, reject) => {
        this.db.get('SELECT COUNT(*) as count FROM books', (err, row) => {
          if (err) reject(err);
          else {
            console.log(`[MCP] SQLite conectado. Livros indexados: ${row.count}`);
            resolve();
          }
        });
      });

    } catch (error) {
      console.error('[MCP] Erro ao inicializar bancos de dados:', error);
      throw error;
    }
  }

  async setup() {
    await this.initializeDatabases();
    this.setupToolHandlers();
  }

  setupToolHandlers() {
    // Listar ferramentas disponíveis
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'rag_search',
          description: 'Busca semântica na base de documentos indexados com links para PDFs',
          inputSchema: {
            type: 'object',
            properties: {
              query: {
                type: 'string',
                description: 'Termo de busca para encontrar documentos relevantes',
              },
              top_k: {
                type: 'number',
                description: 'Número máximo de resultados (padrão: 5)',
                default: 5,
              },
              similarity_threshold: {
                type: 'number',
                description: 'Limiar de similaridade mínimo (padrão: 0.3)',
                default: 0.3,
              },
              include_pdf_links: {
                type: 'boolean',
                description: 'Incluir links clicáveis para abrir PDFs na página específica',
                default: true,
              },
            },
            required: ['query'],
          },
        },
        {
          name: 'rag_list_books',
          description: 'Lista todos os livros indexados na base de dados',
          inputSchema: {
            type: 'object',
            properties: {
              limit: {
                type: 'number',
                description: 'Número máximo de livros para listar (padrão: 20)',
                default: 20,
              },
            },
          },
        },
        {
          name: 'rag_get_book_content',
          description: 'Obtém conteúdo completo ou trechos específicos de um livro',
          inputSchema: {
            type: 'object',
            properties: {
              book_id: {
                type: 'string',
                description: 'ID do livro para obter conteúdo',
              },
              page_numbers: {
                type: 'array',
                items: { type: 'string' },
                description: 'Números das páginas específicas (opcional)',
              },
              chunk_limit: {
                type: 'number',
                description: 'Limite de chunks para retornar (padrão: 10)',
                default: 10,
              },
            },
            required: ['book_id'],
          },
        },
        {
          name: 'rag_open_pdf',
          description: 'Abre um PDF em uma página específica usando visualizador padrão',
          inputSchema: {
            type: 'object',
            properties: {
              book_id: {
                type: 'string',
                description: 'ID do livro para abrir',
              },
              page_number: {
                type: 'number',
                description: 'Número da página para abrir (padrão: 1)',
                default: 1,
              },
            },
            required: ['book_id'],
          },
        },
        {
          name: 'rag_get_stats',
          description: 'Obtém estatísticas da base de dados RAG',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
        {
          name: 'rag_similar_documents',
          description: 'Encontra documentos similares a um texto específico',
          inputSchema: {
            type: 'object',
            properties: {
              text: {
                type: 'string',
                description: 'Texto para encontrar documentos similares',
              },
              top_k: {
                type: 'number',
                description: 'Número máximo de resultados (padrão: 5)',
                default: 5,
              },
            },
            required: ['text'],
          },
        },
      ],
    }));

    // Manipular chamadas de ferramentas
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'rag_search':
            return await this.handleSearch(args);
          case 'rag_list_books':
            return await this.handleListBooks(args);
          case 'rag_get_book_content':
            return await this.handleGetBookContent(args);
          case 'rag_open_pdf':
            return await this.handleOpenPDF(args);
          case 'rag_get_stats':
            return await this.handleGetStats();
          case 'rag_similar_documents':
            return await this.handleSimilarDocuments(args);
          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Ferramenta desconhecida: ${name}`
            );
        }
      } catch (error) {
        console.error(`[MCP] Erro em ${name}:`, error);
        throw new McpError(
          ErrorCode.InternalError,
          `Erro ao executar ${name}: ${error.message}`
        );
      }
    });
  }

  async handleSearch({ query, top_k = 5, similarity_threshold = 0.3, include_pdf_links = true }) {
    try {
      // Gerar embedding da query usando Ollama
      const embedding = await this.generateEmbedding(query);
      
      // Buscar no ChromaDB
      const collection = await this.chromaClient.getCollection({ name: 'document_embeddings' });
      const results = await collection.query({
        queryEmbeddings: [embedding],
        nResults: top_k,
        include: ['documents', 'metadatas', 'distances']
      });

      // Processar resultados
      const searchResults = [];
      
      for (let i = 0; i < results.ids[0].length; i++) {
        const distance = results.distances[0][i];
        const similarity = 1 - distance;
        
        if (similarity < similarity_threshold) continue;

        const metadata = results.metadatas[0][i];
        const bookId = metadata.book_id;
        const page = metadata.page || 'N/A';
        
        // Obter nome e caminho do livro do SQLite
        const bookInfo = await this.getBookInfo(bookId);
        const bookName = bookInfo.name;
        const bookPath = bookInfo.path;
        
        // Extrair parte relevante
        const document = results.documents[0][i];
        const relevantChunk = this.extractRelevantChunk(document, query);
        
        // Criar link para PDF se solicitado
        let pdfLink = null;
        if (include_pdf_links && bookPath && bookPath.toLowerCase().endsWith('.pdf')) {
          const pageNum = parseInt(page) || 1;
          pdfLink = this.createPDFLink(bookPath, pageNum);
        }
        
        searchResults.push({
          query,
          book: bookName,
          book_path: bookPath,
          page,
          similarity: parseFloat(similarity.toFixed(3)),
          relevant_chunk: relevantChunk,
          full_chunk: document,
          book_id: bookId,
          chunk_index: metadata.chunk_index,
          pdf_link: pdfLink,
        });
      }

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              query,
              total_results: searchResults.length,
              results: searchResults,
            }, null, 2),
          },
        ],
      };
    } catch (error) {
      throw new Error(`Erro na busca: ${error.message}`);
    }
  }

  async handleListBooks({ limit = 20 }) {
    return new Promise((resolve, reject) => {
      this.db.all(
        `SELECT id, file_path, file_size, processed_at, chunk_count, embedding_count
         FROM books 
         ORDER BY processed_at DESC
         LIMIT ?`,
        [limit],
        (err, rows) => {
          if (err) {
            reject(new Error(`Erro ao listar livros: ${err.message}`));
          } else {
            const books = rows.map(book => ({
              id: book.id,
              file_path: book.file_path,
              file_size_mb: (book.file_size / (1024 * 1024)).toFixed(1),
              processed_at: book.processed_at,
              chunk_count: book.chunk_count,
              embedding_count: book.embedding_count,
            }));

            resolve({
              content: [
                {
                  type: 'text',
                  text: JSON.stringify({
                    total_books: books.length,
                    books,
                  }, null, 2),
                },
              ],
            });
          }
        }
      );
    });
  }

  async handleGetBookContent({ book_id, page_numbers, chunk_limit = 10 }) {
    return new Promise((resolve, reject) => {
      let query = `
        SELECT chunk_index, content, page_number
        FROM chunks
        WHERE book_id = ?
      `;
      let params = [book_id];

      if (page_numbers && page_numbers.length > 0) {
        query += ` AND page_number IN (${page_numbers.map(() => '?').join(',')})`;
        params = params.concat(page_numbers);
      }

      query += ` ORDER BY chunk_index LIMIT ?`;
      params.push(chunk_limit);

      this.db.all(query, params, (err, rows) => {
        if (err) {
          reject(new Error(`Erro ao obter conteúdo: ${err.message}`));
        } else {
          const chunks = rows.map(row => ({
            chunk_index: row.chunk_index,
            page_number: row.page_number,
            content: row.content,
          }));

          resolve({
            content: [
              {
                type: 'text',
                text: JSON.stringify({
                  book_id,
                  total_chunks: chunks.length,
                  chunks,
                }, null, 2),
              },
            ],
          });
        }
      });
    });
  }

  async handleGetStats() {
    return new Promise((resolve, reject) => {
      this.db.get(
        `SELECT 
           COUNT(*) as total_books,
           SUM(chunk_count) as total_chunks,
           SUM(embedding_count) as total_embeddings,
           AVG(file_size) as avg_file_size
         FROM books`,
        [],
        async (err, bookStats) => {
          if (err) {
            reject(new Error(`Erro ao obter estatísticas: ${err.message}`));
            return;
          }

          try {
            // Obter estatísticas do ChromaDB
            const collection = await this.chromaClient.getCollection({ name: 'document_embeddings' });
            const chromaStats = await collection.count();

            const stats = {
              database: {
                total_books: bookStats.total_books || 0,
                total_chunks: bookStats.total_chunks || 0,
                total_embeddings: bookStats.total_embeddings || 0,
                avg_file_size_mb: bookStats.avg_file_size ? 
                  (bookStats.avg_file_size / (1024 * 1024)).toFixed(2) : 0,
              },
              chroma: {
                indexed_documents: chromaStats,
              },
              config: {
                embedding_model: EMBEDDING_MODEL,
                ollama_host: OLLAMA_HOST,
                data_dir: DATA_DIR,
              },
            };

            resolve({
              content: [
                {
                  type: 'text',
                  text: JSON.stringify(stats, null, 2),
                },
              ],
            });
          } catch (chromaError) {
            reject(new Error(`Erro ao obter estatísticas do ChromaDB: ${chromaError.message}`));
          }
        }
      );
    });
  }

  async handleSimilarDocuments({ text, top_k = 5 }) {
    try {
      // Gerar embedding do texto
      const embedding = await this.generateEmbedding(text);
      
      // Buscar documentos similares
      const collection = await this.chromaClient.getCollection({ name: 'document_embeddings' });
      const results = await collection.query({
        queryEmbeddings: [embedding],
        nResults: top_k,
        include: ['documents', 'metadatas', 'distances']
      });

      // Processar resultados
      const similarDocs = [];
      
      for (let i = 0; i < results.ids[0].length; i++) {
        const distance = results.distances[0][i];
        const similarity = 1 - distance;
        
        const metadata = results.metadatas[0][i];
        const bookId = metadata.book_id;
        const bookName = await this.getBookName(bookId);
        
        similarDocs.push({
          book_id: bookId,
          book_name: bookName,
          page: metadata.page || 'N/A',
          similarity: parseFloat(similarity.toFixed(3)),
          chunk: results.documents[0][i],
        });
      }

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify({
              query_text: text,
              similar_documents: similarDocs,
            }, null, 2),
          },
        ],
      };
    } catch (error) {
      throw new Error(`Erro ao encontrar documentos similares: ${error.message}`);
    }
  }

  async generateEmbedding(text) {
    try {
      const response = await fetch(`${OLLAMA_HOST}/api/embeddings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: EMBEDDING_MODEL,
          prompt: text,
        }),
      });

      if (!response.ok) {
        throw new Error(`Erro na API Ollama: ${response.status}`);
      }

      const data = await response.json();
      return data.embedding;
    } catch (error) {
      throw new Error(`Erro ao gerar embedding: ${error.message}`);
    }
  }

  async getBookInfo(bookId) {
    return new Promise((resolve) => {
      this.db.get(
        'SELECT file_path FROM books WHERE id = ?',
        [bookId],
        (err, row) => {
          if (err || !row) {
            resolve({ name: 'Desconhecido', path: null });
          } else {
            const fileName = row.file_path.split('/').pop() || row.file_path;
            resolve({ name: fileName, path: row.file_path });
          }
        }
      );
    });
  }

  async getBookName(bookId) {
    const info = await this.getBookInfo(bookId);
    return info.name;
  }

  extractRelevantChunk(document, query) {
    // Implementação simples de extração de trecho relevante
    const sentences = document.split(/[.!?]+/);
    const queryWords = query.toLowerCase().split(/\s+/);
    
    let bestSentence = '';
    let bestScore = 0;
    
    for (const sentence of sentences) {
      const sentenceLower = sentence.toLowerCase();
      let score = 0;
      
      for (const word of queryWords) {
        if (sentenceLower.includes(word)) {
          score += 1;
        }
      }
      
      if (score > bestScore && sentence.trim().length > 10) {
        bestScore = score;
        bestSentence = sentence.trim();
      }
    }
    
    return bestSentence || document.substring(0, 200) + '...';
  }

  createPDFLink(bookPath, pageNumber) {
    // Criar link que pode ser clicado para abrir o PDF na página específica
    // Formato: file://[caminho_completo]#page=[numero]
    const absolutePath = require('path').resolve(bookPath);
    return `file://${absolutePath}#page=${pageNumber}`;
  }

  async handleOpenPDF({ book_id, page_number = 1 }) {
    try {
      // Obter caminho do PDF
      const bookInfo = await this.getBookInfo(book_id);
      
      if (!bookInfo.path) {
        throw new Error(`Livro com ID '${book_id}' não encontrado`);
      }

      if (!bookInfo.path.toLowerCase().endsWith('.pdf')) {
        throw new Error(`Livro '${bookInfo.name}' não é um PDF`);
      }

      // Verificar se o arquivo existe
      const fs = require('fs');
      if (!fs.existsSync(bookInfo.path)) {
        throw new Error(`Arquivo PDF não encontrado: ${bookInfo.path}`);
      }

      // Criar link para abrir o PDF na página específica
      const pdfLink = this.createPDFLink(bookInfo.path, page_number);

      // Tentar abrir com o visualizador padrão do sistema
      const { exec } = require('child_process');
      const platform = process.platform;
      
      let command;
      if (platform === 'darwin') {
        // macOS
        command = `open "${bookInfo.path}"`;
      } else if (platform === 'win32') {
        // Windows
        command = `start "" "${bookInfo.path}"`;
      } else {
        // Linux
        command = `xdg-open "${bookInfo.path}"`;
      }

      // Executar comando para abrir o PDF
      exec(command, (error) => {
        if (error) {
          console.error(`[MCP] Erro ao abrir PDF: ${error.message}`);
        }
      });

      return {
        content: [
          {
            type: 'text',
            text: `📂 **PDF Aberto:** ${bookInfo.name}\n📄 **Página:** ${page_number}\n🔗 **Link Direto:** ${pdfLink}\n\n💡 **Dica:** Use o link acima se o PDF não abrir automaticamente.`,
          },
        ],
      };
    } catch (error) {
      throw new Error(`Erro ao abrir PDF: ${error.message}`);
    }
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('[MCP] RAG MCP Server iniciado com sucesso');
  }
}

// Iniciar servidor
const server = new RAGMCPServer();
server.setup().then(() => {
  server.run().catch(console.error);
}).catch(console.error);
