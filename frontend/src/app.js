const { createApp } = Vue;

// API Configuration
const API_BASE_URL = 'https://hackrx-backend-pw4u.onrender.com';

// Document Upload Component
const DocumentUpload = {
    template: `
        <div class="upload-container">
            <div 
                class="upload-drop-zone"
                :class="{ 'drag-over': isDragOver, 'uploading': isUploading, 'success': isSuccess, 'error': uploadError }"
                @dragover.prevent="onDragOver"
                @dragleave.prevent="onDragLeave"
                @drop.prevent="onDrop"
                @click="triggerFileInput"
            >
                <input 
                    ref="fileInput" 
                    type="file" 
                    accept=".pdf,.docx" 
                    @change="onFileSelect" 
                    style="display: none"
                />
                
                <div v-if="isSuccess" class="success-content">
                    <i class="fas fa-check-circle success-icon"></i>
                    <p>Document ready for processing!</p>
                    <small>{{ fileName }}</small>
                </div>
                
                <div v-else-if="isUploading" class="uploading-content">
                    <div class="spinner"></div>
                    <p>Uploading document...</p>
                </div>
                
                <div v-else-if="uploadError" class="error-content">
                    <i class="fas fa-exclamation-triangle error-icon"></i>
                    <p>Upload failed!</p>
                    <small>{{ uploadError }}</small>
                    <button @click="resetUpload" class="retry-btn">Try Again</button>
                </div>
                
                <div v-else class="upload-content">
                    <i class="fas fa-cloud-upload-alt upload-icon"></i>
                    <p>Click or drag & drop your document</p>
                    <small>Supports PDF and DOCX files</small>
                </div>
            </div>
            
            <div class="url-input-section">
                <h3><i class="fas fa-link"></i> Or provide document URL:</h3>
                <div class="url-input-group">
                    <input 
                        v-model="documentUrl" 
                        type="url" 
                        placeholder="Enter document URL here..."
                        class="url-input"
                    />
                    <button @click="processUrl" :disabled="!documentUrl" class="process-btn">
                        <i class="fas fa-play"></i> Process URL
                    </button>
                </div>
            </div>
        </div>
    `,
    data() {
        return {
            isDragOver: false,
            isUploading: false,
            isSuccess: false,
            uploadError: null,
            fileName: '',
            documentUrl: ''
        }
    },
    methods: {
        onDragOver(e) {
            this.isDragOver = true;
        },
        onDragLeave(e) {
            this.isDragOver = false;
        },
        onDrop(e) {
            this.isDragOver = false;
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFile(files[0]);
            }
        },
        triggerFileInput() {
            this.$refs.fileInput.click();
        },
        onFileSelect(e) {
            const file = e.target.files[0];
            if (file) {
                this.handleFile(file);
            }
        },
        async handleFile(file) {
            this.isUploading = true;
            this.uploadError = null;
            this.fileName = file.name;
            
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await axios.post('https://hackrx-backend-pw4u.onrender.com/hackrx/upload', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                
                this.isSuccess = true;
                this.isUploading = false;
                
                // Pass the document_id from the response
                this.$emit('processed', { 
                    url: null, // No URL for local files
                    file: file, // Pass the actual file object
                    type: 'file',
                    document_id: response.data.document_id || 1, // Use real document_id
                    filename: response.data.filename,
                    preview: response.data.text_preview
                });
            } catch (error) {
                console.error('Upload failed:', error);
                this.isUploading = false;
                this.uploadError = error.response?.data?.detail || error.message || 'Upload failed. Please try again.';
            }
        },
        processUrl() {
            if (this.documentUrl) {
                this.isSuccess = true;
                this.uploadError = null;
                this.fileName = 'Document from URL';
                this.$emit('processed', { 
                    url: this.documentUrl, 
                    file: null,
                    type: 'url',
                    document_id: 1, // Default for URL processing
                    filename: 'Document from URL'
                });
            }
        },
        resetUpload() {
            this.uploadError = null;
            this.isSuccess = false;
            this.fileName = '';
        }
    },
    style: `
        <style scoped>
        .upload-container {
            space-y: 20px;
        }
        
        .upload-drop-zone {
            border: 2px dashed #ccc;
            border-radius: 10px;
            padding: 40px 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        
        .upload-drop-zone:hover, .upload-drop-zone.drag-over {
            border-color: #667eea;
            background-color: #f8f9ff;
        }
        
        .upload-drop-zone.success {
            border-color: #27ae60;
            background-color: #f8fff8;
        }
        
        .upload-icon {
            font-size: 3em;
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .success-icon {
            font-size: 3em;
            color: #27ae60;
            margin-bottom: 15px;
        }
        
        .url-input-section h3 {
            margin-bottom: 10px;
            color: #667eea;
        }
        
        .url-input-group {
            display: flex;
            gap: 10px;
        }
        
        .url-input {
            flex: 1;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 14px;
        }
        
        .url-input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .process-btn {
            padding: 12px 20px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: background 0.3s ease;
        }
        
        .process-btn:hover:not(:disabled) {
            background: #5a6fd8;
        }
        
        .process-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        </style>
    `
};

// Query Input Component
const QueryInput = {
    props: ['documentUrl'],
    template: `
        <div class="query-container">
            <div class="custom-questions">
                <h3><i class="fas fa-edit"></i> Your Questions:</h3>
                <div v-for="(question, index) in selectedQuestions" :key="index" class="question-item">
                    <input 
                        v-model="selectedQuestions[index]" 
                        class="question-input"
                        placeholder="Enter your question..."
                    />
                    <button @click="removeQuestion(index)" class="remove-btn">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <button @click="addCustomQuestion" class="add-question-btn">
                    <i class="fas fa-plus"></i> Add Question
                </button>
            </div>
            
            <button 
                @click="processQuestions" 
                :disabled="!documentUrl || selectedQuestions.length === 0"
                class="process-questions-btn"
            >
                <i class="fas fa-play"></i> Process All Questions
            </button>
        </div>
    `,
    data() {
        return {
            selectedQuestions: [''] // Start with one empty question
        }
    },
    methods: {
        addCustomQuestion() {
            this.selectedQuestions.push('');
        },
        removeQuestion(index) {
            this.selectedQuestions.splice(index, 1);
        },
        async processQuestions() {
            if (!this.documentUrl || this.selectedQuestions.length === 0) return;
            
            this.$emit('loading', true);
            
            try {
                // Filter out empty questions
                const validQuestions = this.selectedQuestions.filter(q => q.trim() !== '');
                
                // Prepare payload with real document_id
                const documentId = this.documentUrl.document_id || 1;
                const payload = validQuestions.length === 1 
                    ? { question: validQuestions[0], document_id: documentId }
                    : { questions: validQuestions, document_id: documentId };
                
                console.log('Sending payload:', payload);
                
                const response = await axios.post('https://hackrx-backend-pw4u.onrender.com/hackrx/run', payload, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                console.log('Response from /hackrx/run:', response.data);
                
                // Handle the new HackRx evaluation format
                let answers;
                if (response.data.success && response.data.answers) {
                    answers = response.data.answers;
                } else if (response.data.result) {
                    // Fallback for single question format
                    answers = [{
                        question: validQuestions[0],
                        answer: response.data.result,
                        confidence: response.data.confidence || 0.85
                    }];
                } else {
                    // Error case
                    answers = validQuestions.map(q => ({
                        question: q,
                        answer: response.data.error_message || "Processing failed",
                        confidence: 0.0
                    }));
                }
                
                this.$emit('results', {
                    questions: validQuestions,
                    answers: answers,
                    processing_details: response.data.processing_details || [],
                    success: response.data.success || false
                });
                
            } catch (error) {
                console.error('Processing failed:', error);
                this.$emit('error', 'Failed to process questions: ' + (error.response?.data?.detail || error.message));
            } finally {
                this.$emit('loading', false);
            }
        }
    }
};

// Query Results Component
const QueryResults = {
    props: ['results'],
    template: `
        <div class="results-container">
            <div v-if="results && results.processing_details && results.processing_details.length > 0" class="processing-info">
                <h4><i class="fas fa-cogs"></i> Processing Details:</h4>
                <ul class="processing-list">
                    <li v-for="detail in results.processing_details" :key="detail">{{ detail }}</li>
                </ul>
            </div>
            
            <div v-if="!results || !results.answers || results.answers.length === 0" class="no-results">
                <p>No results to display</p>
                <pre v-if="results">{{ JSON.stringify(results, null, 2) }}</pre>
            </div>
            <div v-else>
                <div v-for="(answer, index) in results.answers" :key="index" class="result-item">
                    <div class="question">
                        <h4><i class="fas fa-question"></i> Question {{ index + 1 }}:</h4>
                        <p>{{ results.questions[index] }}</p>
                    </div>
                    <div class="answer">
                        <h4><i class="fas fa-lightbulb"></i> Answer:</h4>
                        <div class="answer-content" v-html="formatAnswer(answer)"></div>
                        <div class="answer-meta" v-if="answer.confidence !== undefined">
                            <small>Confidence: {{ (answer.confidence * 100).toFixed(1) }}% | Source: {{ answer.source || 'AI Analysis' }}</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,
    mounted() {
        console.log('QueryResults component mounted with results:', this.results);
        console.log('Results type:', typeof this.results);
        console.log('Results.answers:', this.results?.answers);
        console.log('Results.questions:', this.results?.questions);
    },
    methods: {
        formatAnswer(answer) {
            console.log('Raw answer:', answer);
            
            // Handle different answer formats
            let answerText;
            if (typeof answer === 'object' && answer.answer) {
                answerText = answer.answer;
            } else if (typeof answer === 'string') {
                answerText = answer;
            } else {
                answerText = JSON.stringify(answer);
            }
            
            // Format the answer to handle line breaks and improve readability
            const formatted = answerText
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/^\d+\.\s/gm, '<br><strong>$&</strong>')
                .replace(/^(Direct Answer:|Supporting Details:|Relevant Additional Information:)/gm, '<br><strong>$1</strong>');
            console.log('Formatted answer:', formatted);
            return formatted;
        }
    }
};

// Main Vue App
createApp({
    components: {
        DocumentUpload,
        QueryInput,
        QueryResults
    },
    data() {
        return {
            documentUrl: null,
            results: null,
            loading: false,
            error: null
        }
    },
    methods: {
        onDocumentProcessed(data) {
            this.documentUrl = data;
            this.error = null;
        },
        onResults(data) {
            console.log('onResults called with data:', data);
            console.log('Data type:', typeof data);
            console.log('Data.answers:', data?.answers);
            console.log('Data.questions:', data?.questions);
            this.results = data;
            this.error = null;
        },
        onLoading(status) {
            this.loading = status;
        },
        onError(message) {
            this.error = message;
            this.results = null;
        }
    }
}).mount('#app');
