// APK Editor JavaScript functionality

class APKEditor {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupFeatherIcons();
    }

    setupEventListeners() {
        // File upload preview
        const fileInput = document.getElementById('apk_file');
        if (fileInput) {
            fileInput.addEventListener('change', this.handleFileSelect.bind(this));
        }

        // Sign APK buttons
        document.querySelectorAll('.sign-apk-btn').forEach(btn => {
            btn.addEventListener('click', this.handleSignAPK.bind(this));
        });

        // GUI modification form
        const guiForm = document.getElementById('gui-modification-form');
        if (guiForm) {
            guiForm.addEventListener('submit', this.handleGUIModification.bind(this));
        }

        // Generate function form
        const generateForm = document.getElementById('generate-function-form');
        if (generateForm) {
            generateForm.addEventListener('submit', this.handleGenerateFunction.bind(this));
        }

        // Preview functionality
        this.setupPreviewHandlers();
    }

    setupFeatherIcons() {
        // Fix invalid feather icons with valid alternatives
        const iconMappings = {
            'wand': 'zap',
            'palette': 'edit-3',
            'color-palette': 'edit-3',
            'folder-open': 'folder',
            'magic-wand': 'zap',
            'layout': 'grid',
            'lightbulb': 'sun'
        };

        document.querySelectorAll('[data-feather]').forEach(icon => {
            const iconName = icon.getAttribute('data-feather');
            if (iconMappings[iconName]) {
                icon.setAttribute('data-feather', iconMappings[iconName]);
            }
        });

        // Initialize feather icons
        if (typeof feather !== 'undefined') {
            feather.replace();
        }
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            const fileSize = (file.size / (1024 * 1024)).toFixed(2);
            console.log(`Selected APK: ${file.name} (${fileSize} MB)`);

            // Update UI to show selected file
            const fileInfo = document.getElementById('file-info');
            if (fileInfo) {
                fileInfo.textContent = `${file.name} (${fileSize} MB)`;
                fileInfo.style.display = 'block';
            }

            // Show success notification
            this.showNotification(`Selected: ${file.name} (${fileSize} MB)`, 'info');
        }
    }

    handleSignAPK(event) {
        const projectId = event.target.getAttribute('data-project-id');
        if (!projectId) return;

        // Show loading state
        const btn = event.target;
        const originalText = btn.textContent;
        btn.textContent = 'Signing...';
        btn.disabled = true;

        // Make AJAX request to sign APK
        fetch(`/sign_apk/${projectId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showNotification('APK signed successfully!', 'success');
                // Reload page to update UI
                setTimeout(() => location.reload(), 1000);
            } else {
                this.showNotification(`Signing failed: ${data.message}`, 'error');
            }
        })
        .catch(error => {
            this.showNotification('Signing failed: Network error', 'error');
            console.error('Sign APK error:', error);
        })
        .finally(() => {
            btn.textContent = originalText;
            btn.disabled = false;
        });
    }

    handleGUIModification(event) {
        // Add loading overlay
        this.showLoadingOverlay('Applying GUI modifications...');

        const button = event.target.querySelector('button[type="submit"]');
        if (button) {
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Applying Changes...';
        }
    }

    handleGenerateFunction(event) {
        // Add loading overlay
        this.showLoadingOverlay('Generating Android code...');

        const button = event.target.querySelector('button[type="submit"]');
        if (button) {
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
        }
    }

    setupPreviewHandlers() {
        // Real-time preview updates
        const guiChangesInput = document.getElementById('gui_changes');
        const colorSchemeSelect = document.getElementById('color_scheme');

        if (guiChangesInput) {
            guiChangesInput.addEventListener('input', this.updatePreview.bind(this));
        }

        if (colorSchemeSelect) {
            colorSchemeSelect.addEventListener('change', this.updatePreview.bind(this));
        }
    }

    updatePreview() {
        const guiChanges = document.getElementById('gui_changes')?.value || '';
        const colorScheme = document.getElementById('color_scheme')?.value || '';

        // Update preview elements
        const previewButton = document.getElementById('preview-button');
        const previewText = document.getElementById('preview-text');
        const previewStatus = document.getElementById('preview-status');

        if (previewButton) {
            // Apply color scheme to preview button
            const colorMap = {
                'blue': '#007bff',
                'green': '#28a745', 
                'red': '#dc3545',
                'purple': '#6f42c1',
                'orange': '#fd7e14',
                'dark': '#343a40',
                'light': '#f8f9fa'
            };

            if (colorScheme && colorMap[colorScheme]) {
                previewButton.style.backgroundColor = colorMap[colorScheme];
                previewButton.style.borderColor = colorMap[colorScheme];
            }
        }

        // Update preview text based on changes
        if (previewText && guiChanges) {
            if (guiChanges.toLowerCase().includes('button')) {
                previewText.textContent = 'Button preview updated';
            } else if (guiChanges.toLowerCase().includes('color')) {
                previewText.textContent = 'Color scheme preview';
            } else {
                previewText.textContent = 'GUI changes preview';
            }
        }

        // Update connection status if mentioned
        if (previewStatus && guiChanges.toLowerCase().includes('connect')) {
            if (guiChanges.toLowerCase().includes('disconnect')) {
                previewStatus.textContent = 'Status: Disconnected';
                previewStatus.className = 'preview-status text-danger';
            } else {
                previewStatus.textContent = 'Status: Connected';
                previewStatus.className = 'preview-status text-success';
            }
        }
    }

    showLoadingOverlay(message = 'Processing...') {
        // Remove existing overlay
        const existingOverlay = document.querySelector('.loading-overlay');
        if (existingOverlay) {
            existingOverlay.remove();
        }

        // Create loading overlay
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 mb-0">${message}</p>
            </div>
        `;

        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.7);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        `;

        document.body.appendChild(overlay);
    }

    hideLoadingOverlay() {
        const overlay = document.querySelector('.loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        notification.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;';

        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Utility functions
    copyToClipboard(text) {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success');
            }).catch(err => {
                console.log('Failed to copy: ', err);
                this.fallbackCopyTextToClipboard(text);
            });
        } else {
            this.fallbackCopyTextToClipboard(text);
        }
    }

    fallbackCopyTextToClipboard(text) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.cssText = "top: 0; left: 0; position: fixed;";

        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        try {
            const successful = document.execCommand('copy');
            if (successful) {
                this.showNotification('Copied to clipboard!', 'success');
            }
        } catch (err) {
            console.log('Failed to copy: ', err);
        }

        document.body.removeChild(textArea);
    }
}

// Initialize the APK Editor when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    new APKEditor();
});
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.APKEditor = new APKEditor();
});

// Global functions for HTML onclick handlers
function showAPKToolInfo() {
    if (typeof bootstrap !== 'undefined' && document.getElementById('apktoolModal')) {
        const modal = new bootstrap.Modal(document.getElementById('apktoolModal'));
        modal.show();
    }
}

function browseForStudioPath() {
    // Since we can't actually browse files in web, provide platform-specific hints
    const platform = navigator.platform.toLowerCase();
    let suggestion = '';
    
    if (platform.includes('win')) {
        suggestion = 'C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe';
    } else if (platform.includes('mac')) {
        suggestion = '/Applications/Android Studio.app/Contents/MacOS/studio';
    } else {
        suggestion = '/opt/android-studio/bin/studio.sh';
    }
    
    const input = document.getElementById('android_studio_path');
    if (input && !input.value) {
        input.value = suggestion;
    }
    
    // Show helpful modal
    showStudioPathModal();
}

function showStudioPathModal() {
    const modalHTML = `
        <div class="modal fade" id="studioPathModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i data-feather="folder"></i>
                            Find Android Studio Path
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <h6>Common Android Studio Locations:</h6>
                        <div class="mb-3">
                            <strong>Windows:</strong>
                            <ul class="small">
                                <li><code>C:\\Program Files\\Android\\Android Studio\\bin\\studio64.exe</code></li>
                                <li><code>C:\\Users\\[Username]\\AppData\\Local\\Android\\Studio\\bin\\studio64.exe</code></li>
                            </ul>
                        </div>
                        <div class="mb-3">
                            <strong>macOS:</strong>
                            <ul class="small">
                                <li><code>/Applications/Android Studio.app/Contents/MacOS/studio</code></li>
                            </ul>
                        </div>
                        <div class="mb-3">
                            <strong>Linux:</strong>
                            <ul class="small">
                                <li><code>/opt/android-studio/bin/studio.sh</code></li>
                                <li><code>~/android-studio/bin/studio.sh</code></li>
                            </ul>
                        </div>
                        <div class="alert alert-info">
                            <small>Copy the full path to the executable file and paste it in the configuration field.</small>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal
    const existingModal = document.getElementById('studioPathModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('studioPathModal'));
    modal.show();
    
    // Replace feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function showAntivirusHelp() {
    const modalHTML = `
        <div class="modal fade" id="antivirusHelpModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i data-feather="shield"></i>
                            Antivirus Configuration - Prevent Wacatac.B!ml Detection
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-warning">
                            <strong>Why are APK tools detected as malware?</strong><br>
                            Tools like apktool.jar are legitimate Android development utilities, but antivirus software may flag them as 
                            Trojan:Script/Wacatac.B!ml due to their ability to modify Android applications.
                        </div>
                        
                        <h6>Required Exclusions:</h6>
                        <div class="row">
                            <div class="col-md-6">
                                <h6>Folders to Exclude:</h6>
                                <ul class="small">
                                    <li><code>${window.location.origin}</code></li>
                                    <li><code>projects/</code></li>
                                    <li><code>tools/</code></li>
                                    <li><code>temp/</code></li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6>File Types:</h6>
                                <ul class="small">
                                    <li><code>*.apk</code> files</li>
                                    <li><code>apktool.jar</code></li>
                                    <li><code>adb.exe</code></li>
                                    <li><code>*.jar</code> files in tools/</li>
                                </ul>
                            </div>
                        </div>
                        
                        <h6>Windows Defender Instructions:</h6>
                        <ol class="small">
                            <li>Open Windows Security</li>
                            <li>Go to "Virus & threat protection"</li>
                            <li>Click "Manage settings" under "Virus & threat protection settings"</li>
                            <li>Click "Add or remove exclusions"</li>
                            <li>Add folder exclusions for the paths above</li>
                        </ol>
                        
                        <div class="alert alert-info mt-3">
                            <strong>Safe Usage:</strong> These tools are used only for legitimate Android development. 
                            The exclusions ensure smooth operation while maintaining system security.
                        </div>
                    </div>
                    <div class="modal-footer">
                        <a href="/antivirus_help" class="btn btn-primary">
                            <i data-feather="external-link"></i>
                            Detailed Guide
                        </a>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal
    const existingModal = document.getElementById('antivirusHelpModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('antivirusHelpModal'));
    modal.show();
    
    // Replace feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}

function testAI() {
    fetch('/test_ai', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.APKEditor.showNotification('AI test successful!', 'success');
        } else {
            window.APKEditor.showNotification(`AI test failed: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        window.APKEditor.showNotification('AI test failed: Network error', 'error');
    });
}

// Output Folder Management Functions
function openOutputFolder(projectId) {
    fetch(`/open_output_folder/${projectId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.APKEditor.showNotification('Opening output folder in Explorer...', 'success');
        } else {
            window.APKEditor.showNotification(`Failed to open folder: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        window.APKEditor.showNotification('Failed to open folder: Network error', 'error');
    });
}

function copyOutputPath(projectId) {
    const path = `projects/${projectId}/decompiled/`;
    const fullPath = `${window.location.origin}/${path}`;

    if (window.APKEditor) {
        window.APKEditor.copyToClipboard(fullPath);
    } else {
        // Fallback
        navigator.clipboard.writeText(fullPath).then(() => {
            alert('Path copied to clipboard!');
        }).catch(() => {
            alert(`Path: ${fullPath}`);
        });
    }
}

function showOutputInfo(projectId) {
    fetch(`/get_output_info/${projectId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showOutputInfoModal(data.info);
        } else {
            window.APKEditor.showNotification(`Failed to get folder info: ${data.message}`, 'error');
        }
    })
    .catch(error => {
        window.APKEditor.showNotification('Failed to get folder info: Network error', 'error');
    });
}

// Handle project actions
function openOutputFolder(projectId) {
    fetch(`/open_output_folder/${projectId}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to open output folder', 'error');
    });
}

function openResourceFolder(projectId, resourceType) {
    fetch(`/open_resource_folder/${projectId}/${resourceType}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
        } else {
            showNotification(data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Failed to open ' + resourceType + ' folder', 'error');
    });
}

function exportProject(projectId, exportType) {
    window.APKEditor.showLoadingOverlay(`Exporting project as ${exportType.toUpperCase()}...`);

    fetch(`/export_project/${projectId}/${exportType}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('Export failed');
    })
    .then(blob => {
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `project_${projectId}_${exportType}.zip`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        window.APKEditor.showNotification(`Project exported successfully!`, 'success');
    })
    .catch(error => {
        window.APKEditor.showNotification(`Export failed: ${error.message}`, 'error');
    })
    .finally(() => {
        window.APKEditor.hideLoadingOverlay();
    });
}

function showOutputInfoModal(info) {
    // Create modal HTML
    const modalHTML = `
        <div class="modal fade" id="outputInfoModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i data-feather="info"></i>
                            Output Folder Information
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6><i data-feather="folder"></i> Folder Details</h6>
                                <ul class="list-unstyled">
                                    <li><strong>Path:</strong> <code>${info.path}</code></li>
                                    <li><strong>Size:</strong> ${info.size}</li>
                                    <li><strong>Files:</strong> ${info.file_count}</li>
                                    <li><strong>Created:</strong> ${info.created}</li>
                                </ul>
                            </div>
                            <div class="col-md-6">
                                <h6><i data-feather="file"></i> Contents</h6>
                                <div class="row text-center">
                                    <div class="col-4">
                                        <div class="border rounded p-2">
                                            <i data-feather="image" class="text-primary"></i>
                                            <div><strong>${info.resources.images || 0}</strong></div>
                                            <small>Images</small>
                                        </div>
                                    </div>
                                    <div class="col-4">
                                        <div class="border rounded p-2">
                                            <i data-feather="code" class="text-warning"></i>
                                            <div><strong>${info.resources.smali || 0}</strong></div>
                                            <small>Smali</small>
                                        </div>
                                    </div>
                                    <div class="col-4">
                                        <div class="border rounded p-2">
                                            <i data-feather="layout" class="text-success"></i>
                                            <div><strong>${info.resources.layouts || 0}</strong></div>
                                            <small>Layouts</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <hr>
                        <div class="text-center">
                            <button class="btn btn-primary" onclick="copyOutputPath('${info.project_id}')">
                                <i data-feather="copy"></i>
                                Copy Path
                            </button>
                            <button class="btn btn-success" onclick="openOutputFolder('${info.project_id}')">
                                <i data-feather="external-link"></i>
                                Open Folder
                            </button>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remove existing modal
    const existingModal = document.getElementById('outputInfoModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('outputInfoModal'));
    modal.show();

    // Replace feather icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
}