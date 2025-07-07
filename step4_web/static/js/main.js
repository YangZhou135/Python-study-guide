// 主要JavaScript功能

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化所有功能
    initializeApp();
});

// 初始化应用
function initializeApp() {
    // 添加淡入动画
    addFadeInAnimation();
    
    // 初始化工具提示
    initializeTooltips();
    
    // 初始化表单验证
    initializeFormValidation();
    
    // 初始化图片懒加载
    initializeLazyLoading();
    
    // 初始化搜索功能
    initializeSearch();
    
    console.log('✅ 应用初始化完成');
}

// 添加淡入动画
function addFadeInAnimation() {
    const elements = document.querySelectorAll('.card, .article-card');
    elements.forEach((element, index) => {
        element.style.animationDelay = `${index * 0.1}s`;
        element.classList.add('fade-in');
    });
}

// 初始化工具提示
function initializeTooltips() {
    // 如果Bootstrap的tooltip可用
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// 初始化表单验证
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // 实时验证
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });
}

// 验证单个字段
function validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const name = field.name;
    
    // 清除之前的错误
    clearFieldError(field);
    
    // 基本验证
    if (field.hasAttribute('required') && !value) {
        showFieldError(field, '此字段不能为空');
        return false;
    }
    
    // 邮箱验证
    if (type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            showFieldError(field, '请输入有效的邮箱地址');
            return false;
        }
    }
    
    // 密码验证
    if (name === 'password' && value) {
        if (value.length < 6) {
            showFieldError(field, '密码长度至少6个字符');
            return false;
        }
    }
    
    // 确认密码验证
    if (name === 'password2' && value) {
        const password = document.querySelector('input[name="password"]');
        if (password && value !== password.value) {
            showFieldError(field, '两次输入的密码不一致');
            return false;
        }
    }
    
    return true;
}

// 显示字段错误
function showFieldError(field, message) {
    field.classList.add('is-invalid');
    
    let errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        field.parentNode.appendChild(errorDiv);
    }
    errorDiv.textContent = message;
}

// 清除字段错误
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// 初始化图片懒加载
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // 降级处理
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// 初始化搜索功能
function initializeSearch() {
    const searchInput = document.querySelector('input[name="query"]');
    if (searchInput) {
        // 搜索建议功能（简单实现）
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // 这里可以添加搜索建议功能
                console.log('搜索:', this.value);
            }, 300);
        });
    }
}

// 工具函数

// 显示加载状态
function showLoading(element) {
    const originalContent = element.innerHTML;
    element.innerHTML = '<span class="loading"></span> 加载中...';
    element.disabled = true;
    
    return function hideLoading() {
        element.innerHTML = originalContent;
        element.disabled = false;
    };
}

// 显示提示消息
function showToast(message, type = 'info', duration = 3000) {
    // 创建提示元素
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    // 自动移除
    setTimeout(() => {
        if (toast.parentNode) {
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 150);
        }
    }, duration);
}

// 确认对话框
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// 复制到剪贴板
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('已复制到剪贴板', 'success');
        }).catch(() => {
            showToast('复制失败', 'error');
        });
    } else {
        // 降级处理
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast('已复制到剪贴板', 'success');
        } catch (err) {
            showToast('复制失败', 'error');
        }
        document.body.removeChild(textArea);
    }
}

// 格式化日期
function formatDate(date) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(date).toLocaleDateString('zh-CN', options);
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// AJAX请求封装
function request(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const config = { ...defaultOptions, ...options };
    
    return fetch(url, config)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Request failed:', error);
            showToast('网络请求失败', 'error');
            throw error;
        });
}

// 文章相关功能
const ArticleUtils = {
    // 点赞文章
    like: function(articleId) {
        return request(`/api/article/${articleId}/like`, { method: 'POST' })
            .then(data => {
                if (data.success) {
                    // 更新点赞数显示
                    const likesElement = document.getElementById('likes-count');
                    if (likesElement) {
                        likesElement.textContent = data.likes;
                    }
                    showToast('点赞成功！', 'success');
                } else {
                    showToast('点赞失败', 'error');
                }
                return data;
            });
    },
    
    // 分享文章
    share: function(title, url) {
        if (navigator.share) {
            navigator.share({
                title: title,
                url: url
            }).catch(err => console.log('分享失败:', err));
        } else {
            copyToClipboard(url);
        }
    }
};

// 表单相关功能
const FormUtils = {
    // 自动保存草稿
    autoSave: function(formId, interval = 30000) {
        const form = document.getElementById(formId);
        if (!form) return;
        
        setInterval(() => {
            const formData = new FormData(form);
            const data = Object.fromEntries(formData);
            localStorage.setItem(`draft_${formId}`, JSON.stringify(data));
            console.log('草稿已自动保存');
        }, interval);
    },
    
    // 恢复草稿
    restoreDraft: function(formId) {
        const draft = localStorage.getItem(`draft_${formId}`);
        if (!draft) return;
        
        try {
            const data = JSON.parse(draft);
            const form = document.getElementById(formId);
            
            Object.keys(data).forEach(key => {
                const field = form.querySelector(`[name="${key}"]`);
                if (field) {
                    field.value = data[key];
                }
            });
            
            showToast('已恢复草稿', 'info');
        } catch (err) {
            console.error('恢复草稿失败:', err);
        }
    },
    
    // 清除草稿
    clearDraft: function(formId) {
        localStorage.removeItem(`draft_${formId}`);
    }
};

// 导出到全局作用域
window.showToast = showToast;
window.confirmAction = confirmAction;
window.copyToClipboard = copyToClipboard;
window.ArticleUtils = ArticleUtils;
window.FormUtils = FormUtils;
