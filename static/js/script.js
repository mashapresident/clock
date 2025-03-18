document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("set_steps").addEventListener("submit", function (event) {
        let stepsInput = document.getElementById("steps_per_revolution");
        let stepsValue = parseInt(stepsInput.value, 10);

        if (isNaN(stepsValue) || stepsValue < 0) {
            alert("Кількість кроків на оберт повинна бути невід’ємним числом!");
            event.preventDefault();
        }
    });
});

