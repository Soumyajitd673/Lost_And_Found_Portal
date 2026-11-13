document.addEventListener('DOMContentLoaded', () => {
    const role = (document.body.dataset.role || 'student').toLowerCase();
    const adminBtn = document.getElementById('adminBtn');
    const profileBtn = document.getElementById('profileBtn');
    const roleBadge = document.getElementById('userRole');
 
    if (roleBadge) {
        roleBadge.textContent = role.charAt(0).toUpperCase() + role.slice(1);
        roleBadge.classList.toggle('student-role', role === 'student');
        roleBadge.classList.toggle('admin-role', role === 'admin');
    }
 
    if (adminBtn && role === 'admin') {
        adminBtn.classList.remove('hidden');
        adminBtn.addEventListener('click', () => {
            window.location.href = '/admin/dashboard'; 
        });
    }
 
    if (profileBtn) {
        profileBtn.addEventListener('click', () => {
            window.location.href = '/user/profile'; 
        });
    }
  
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            document.getElementById(btn.getAttribute('data-target')).classList.add('active');
        });
    });  

    function formatDate(value) {
        const d = new Date(value);
        if (isNaN(d.getTime())) return 'Unknown date';
        return d.toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' });
    }
 
    function showMessage(listEl, text) {
        listEl.replaceChildren();      
        const li = document.createElement('li');
        li.style.justifyContent = 'center';
        li.style.color = '#64748b';
        li.textContent = text;
        listEl.appendChild(li);
    }
 
    function renderList(listEl, items, emptyMessage) {
        if (!listEl) return;
        listEl.replaceChildren();
 
        if (!Array.isArray(items) || items.length === 0) {
            showMessage(listEl, emptyMessage);
            return;
        }
 
        items.forEach(item => {
            const li = document.createElement('li');
 
            const title = document.createElement('span');
            title.className = 'item-title';
            title.textContent = item.item_name;
 
            const date = document.createElement('span');
            date.className = 'item-date';
            date.textContent = formatDate(item.date_reported);
 
            li.append(title, date);
            listEl.appendChild(li);
        });
    }
 
    async function fetchUserHistory() {
        const lostList = document.querySelector('#lostHistory .item-list');
        const foundList = document.querySelector('#foundHistory .item-list');
 
        try {
            const response = await fetch('/api/user/history');
            if (!response.ok) {
                throw new Error(`Server responded with status ${response.status}`);
            }
 
            const data = await response.json();
 
            renderList(lostList, data.lostItems, 'No lost items reported yet.');
            renderList(foundList, data.foundItems, 'No found items reported yet.');
 
        } catch (error) {
            console.error('Error fetching history:', error);
            showMessage(lostList, 'Error loading data...');
            showMessage(foundList, 'Error loading data...');
        }
    }
 
    fetchUserHistory();

    const deleteBtn = document.getElementById('deleteAccountBtn');
    const deleteModal = document.getElementById('deleteModal');
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const passwordInput = document.getElementById('deletePasswordInput');
    const errorMsg = document.getElementById('passwordErrorMsg');
 
    const showError = (text) => {
        if (!errorMsg) return;
        errorMsg.textContent = text;
        errorMsg.classList.remove('hidden');
    };
 
    const closeModal = () => {
        if (deleteModal) deleteModal.classList.add('hidden');
        if (passwordInput) passwordInput.value = '';
        if (errorMsg) errorMsg.classList.add('hidden');
        if (confirmDeleteBtn) {
            confirmDeleteBtn.disabled = false;
            confirmDeleteBtn.textContent = 'Verify & Delete';
        }
    };

    if (deleteBtn) {
        deleteBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (deleteModal) deleteModal.classList.remove('hidden');
            if (passwordInput) passwordInput.focus();
        });
    }

    if (cancelDeleteBtn) {
        cancelDeleteBtn.addEventListener('click', (e) => {
            e.preventDefault();
            closeModal();
        });
    }
 

    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', async (e) => {
            e.preventDefault();
 
            const enteredPassword = passwordInput.value.trim();
 
            if (!enteredPassword) {
                showError('Password is required!');
                return;
            }
 
            errorMsg.classList.add('hidden');

            confirmDeleteBtn.disabled = true;
            confirmDeleteBtn.textContent = 'Deleting...';
 
            try {
                const res = await fetch('/api/user/delete', {
                    method: 'DELETE',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ password: enteredPassword })
                });
 
                let result = {};
                try { result = await res.json(); } catch (_) {}
 
                if (res.ok) {
                    window.location.href = '/user/login';
                } else {
                    showError(result.message || 'Could not delete account. Please try again.');
                    confirmDeleteBtn.disabled = false;
                    confirmDeleteBtn.textContent = 'Verify & Delete';
                }
 
            } catch (error) {
                console.error('Delete account error:', error);
                showError('Network error. Please try again.');
                confirmDeleteBtn.disabled = false;
                confirmDeleteBtn.textContent = 'Verify & Delete';
            }
        });
    }
 
    if (passwordInput && confirmDeleteBtn) {
        passwordInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') confirmDeleteBtn.click();
        });
    }
 
    window.addEventListener('click', (event) => {
        if (event.target === deleteModal) closeModal();
    });
 
});