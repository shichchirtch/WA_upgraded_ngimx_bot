document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Главная страница загружена!");
    if (window.Telegram && Telegram.WebApp) {
        console.log("✅ Telegram WebApp API подключен");
        const initData = Telegram.WebApp.initDataUnsafe;
        console.log("📦 Данные от Telegram:", initData);
        const HOST_PATH='https://fe2d-2a00-20-5-96e1-a933-df32-3f83-7e19.ngrok-free.app'
        fetch(`${HOST_PATH}/receive_telegram_data`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(initData)
        })
        .then(response => response.json())
        .then(data => console.log("✅ Сервер ответил:", data))
        .catch(error => console.error("❌ Ошибка при отправке:", error));

        // Сохраняем в localStorage
        localStorage.setItem("telegramData", JSON.stringify(initData));
    } else {
        console.warn("⚠️ Telegram WebApp API не подключен!");
    }


    // Логика перехода по картинкам (если нужно)
    document.querySelectorAll(".pizza-list a").forEach(link => {
        link.addEventListener("click", function (event) {
            console.log(`➡️ Переход к пицце: ${this.href}`);
        });
    });
});
