document.getElementById("question-form").addEventListener("submit", function (event) {
    event.preventDefault();
    const topic = document.getElementById("topic").value;
    const questionType = document.querySelector('input[name="question-type"]:checked').value;

    fetch('/generate_questions', {
        method: 'POST',
        body: new URLSearchParams({ 'topic': topic, 'questionType': questionType }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        const questionsDiv = document.getElementById("questions");
        questionsDiv.innerHTML = '';

        if (data.questions) {
            data.questions.forEach(function (question, index) {
                const questionElement = document.createElement("p");
                questionElement.textContent = `${question}`;
                questionsDiv.appendChild(questionElement);
            });
        } else if (data.error) {
            const errorElement = document.createElement("p");
            errorElement.textContent = `Error: ${data.error}`;
            questionsDiv.appendChild(errorElement);
        }
    })
    .catch(error => {
        const questionsDiv = document.getElementById("questions");
        questionsDiv.innerHTML = '';

        const errorElement = document.createElement("p");
        errorElement.textContent = `An error occurred: ${error.message}`;
        questionsDiv.appendChild(errorElement);
    });
});
