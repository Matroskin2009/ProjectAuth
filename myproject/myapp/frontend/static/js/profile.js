document.addEventListener('DOMContentLoaded', function() {
    // Создание звездного фона
    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.classList.add('star');
        star.style.width = `${Math.random() * 3}px`;
        star.style.height = star.style.width;
        star.style.left = `${Math.random() * 100}vw`;
        star.style.top = `${Math.random() * 100}vh`;
        star.style.animationDelay = `${Math.random() * 5}s`;
        document.body.appendChild(star);
    }

    // Создание комет
    for (let i = 0; i < 3; i++) {
        const comet = document.createElement('div');
        comet.classList.add('comet');
        comet.style.top = `${Math.random() * 100}vh`;
        comet.style.left = `${Math.random() * 100}vw`;
        comet.style.animationDelay = `${Math.random() * 10}s`;
        comet.style.animationDuration = `${10 + Math.random() * 20}s`;
        document.body.appendChild(comet);
    }

    // Обработка активации инвайт-кода
    const activateBtn = document.getElementById('activate-invite-btn');
    const inviteInput = document.getElementById('invite-code-input');
    const messageElement = document.getElementById('invite-message');
    const inviteSection = document.getElementById('activate-invite-section');

    // Проверяем только необходимые элементы
    if (!activateBtn || !inviteInput || !messageElement || !inviteSection) {
        console.error('Один из необходимых элементов не найден:',
            {activateBtn, inviteInput, messageElement, inviteSection});
        return;
    }

    activateBtn.addEventListener('click', function() {
        const code = inviteInput.value.trim();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        const url = document.body.dataset.urlAddInviter;

        if (!code) {
            messageElement.textContent = 'Введите код!';
            messageElement.style.color = '#f44336';
            return;
        }

        if (!csrfToken) {
            console.error('CSRF токен не найден');
            messageElement.textContent = 'Ошибка безопасности. Перезагрузите страницу.';
            messageElement.style.color = '#f44336';
            return;
        }

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `inviter=${encodeURIComponent(code)}`
        })
        .then(response => {
        return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                messageElement.textContent = data.message;
                messageElement.style.color = '#4caf50';

                setTimeout(() => {
                    inviteSection.innerHTML = `
                        <p>Активированный код: <span id="activated-invite">${code}</span></p>
                    `;
                }, 1000);
            } else {
                messageElement.textContent = data.message || 'Произошла ошибка';
                messageElement.style.color = '#f44336';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            messageElement.textContent = 'Ошибка при активации кода';
            messageElement.style.color = '#f44336';
        });
    });
});