const timer = document.getElementById("timer");
const quizForm = document.getElementById("quiz-form");

if (timer && quizForm) {
    let timeLeft = 10 * 60;

    const countdown = setInterval(function() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;

        timer.textContent =
            String(minutes).padStart(2, "0") + ":" +
            String(seconds).padStart(2, "0");

        if (timeLeft <= 60) {
            timer.classList.add("warning");
        }

        if (timeLeft <= 0) {
            clearInterval(countdown);
            quizForm.submit();
            return;
        }

        timeLeft--;
    }, 1000);
    const fullscreenButton = document.getElementById("fullscreen-button");
const warning = document.getElementById("integrity-warning");

function showWarning(message) {
    if (warning) {
        warning.textContent = message;
        warning.classList.add("show");

        setTimeout(function() {
            warning.classList.remove("show");
        }, 3000);
    }
}

if (fullscreenButton) {
    fullscreenButton.addEventListener("click", function() {
        document.documentElement.requestFullscreen().catch(function() {
            showWarning("FULLSCREEN COULD NOT BE ENABLED.");
        });

        fullscreenButton.textContent = "FULLSCREEN ACTIVE";
    });
}

document.addEventListener("fullscreenchange", function() {
    if (!document.fullscreenElement) {
        showWarning("WARNING! PLEASE RETURN TO FULLSCREEN.");
    }
});

document.addEventListener("visibilitychange", function() {
    if (document.hidden) {
        showWarning("WARNING! DO NOT LEAVE THE QUIZ TAB.");
    }
});

document.addEventListener("copy", function(event) {
    event.preventDefault();
    showWarning("COPYING IS DISABLED DURING THE QUIZ.");
});

document.addEventListener("cut", function(event) {
    event.preventDefault();
    showWarning("CUTTING IS DISABLED DURING THE QUIZ.");
});

document.addEventListener("paste", function(event) {
    event.preventDefault();
    showWarning("PASTING IS DISABLED DURING THE QUIZ.");
});

document.addEventListener("contextmenu", function(event) {
    event.preventDefault();
    showWarning("RIGHT CLICK IS DISABLED DURING THE QUIZ.");
});
}