
alert(url)
document.addEventListener('DOMContentLoaded', function() {
    const url_get_key = document.body.dataset.urlGetKey;
    const url_profile_page = document.body.dataset.urlProfilePage
    const url_unified_auth = document.body.dataset.urlUnifiedAuth;
    const button_back = document.querySelector('.get-back');
    const authButton = document.getElementById('auth-button');
    let check_number_button = document.getElementById('check-number-button');
    let key = 0;

    for (let i = 0; i < 200; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.cssText = `
            width: ${1 + Math.random() * 4}px;
            height: ${1 + Math.random() * 4}px;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            animation-duration: ${3 + Math.random() * 15}s;
            animation-delay: ${Math.random() * 20}s;
            opacity: ${0.7 + Math.random() * 0.3};
        `;
        document.body.appendChild(star);
    }

    authButton.addEventListener('click', () => {
        fetch(url_get_key, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('#auth-form [name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => {
            if (!response.ok) throw new Error('Ошибка сервера');
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                document.getElementById('login-screen')?.classList.add('hidden');
                document.getElementById('sms-screen')?.classList.remove('hidden');
                key = data.key;
            } else {
                document.getElementById('message').textContent = data.message || 'Ошибка авторизации';
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            document.getElementById('message').textContent = 'Ошибка соединения';
        });
    });

    check_number_button.addEventListener('click', () => {
    const form = document.getElementById('auth-form');
    const formData = new FormData(form);
    formData.append('user_key', document.getElementById('number-phone-check').value);
    formData.append('right_key', key);

    fetch(url_unified_auth, {
        method: 'POST',
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error('Ошибка сервера');
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            alert(url_profile_page)
            window.location.href = url;
        } else {
            document.getElementById('message-number').textContent = data.message || 'Неверный код';
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('message-number').textContent = 'Ошибка проверки кода';
    });
});

    if (button_back) {
        button_back.addEventListener('click', (e) => {
            e.preventDefault();
            document.getElementById('login-screen')?.classList.add('hidden');
            document.getElementById('sms-screen')?.classList.remove('hidden');
        });
    }
});