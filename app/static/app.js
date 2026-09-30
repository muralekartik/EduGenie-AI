async function sendRequest(url, data) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
    }

    return await response.json();
}


function showLoading(element) {
    element.innerHTML = "⏳ Thinking...";
}


function showError(element, error) {
    element.innerHTML = `❌ ${error.message}`;
}


async function askQuestion() {
    const question = document.getElementById("qnaQuestion").value.trim();
    const context = document.getElementById("qnaContext").value.trim();
    const result = document.getElementById("qnaResult");

    if (!question) {
        result.innerHTML = "Please enter a question.";
        return;
    }

    showLoading(result);

    try {
        const data = await sendRequest("/api/qna", {
            question: question,
            context: context
        });

        result.innerHTML = `
            <strong>Answer:</strong><br><br>
            ${escapeHtml(data.answer)}
            <br><br>
            <small>Source: ${escapeHtml(data.source || "EduGenie")}</small>
        `;
    } catch (error) {
        showError(result, error);
    }
}


async function explainTopic() {
    const topic = document.getElementById("explainTopic").value.trim();
    const level = document.getElementById("explainLevel").value;
    const result = document.getElementById("explainResult");

    if (!topic) {
        result.innerHTML = "Please enter a topic.";
        return;
    }

    showLoading(result);

    try {
        const data = await sendRequest("/api/explain", {
            topic: topic,
            level: level
        });

        result.innerHTML = `
            <strong>${escapeHtml(data.topic)}</strong>
            <br><br>
            ${formatText(data.explanation)}
            <br><br>
            <small>Source: ${escapeHtml(data.source || "EduGenie")}</small>
        `;
    } catch (error) {
        showError(result, error);
    }
}


async function summarizeText() {
    const text = document.getElementById("summaryText").value.trim();
    const length = document.getElementById("summaryLength").value;
    const result = document.getElementById("summaryResult");

    if (!text) {
        result.innerHTML = "Please enter some text.";
        return;
    }

    showLoading(result);

    try {
        const data = await sendRequest("/api/summarize", {
            text: text,
            length: length
        });

        result.innerHTML = `
            <strong>Summary:</strong><br><br>
            ${escapeHtml(data.summary)}
            <br><br>
            <small>Source: ${escapeHtml(data.source || "EduGenie")}</small>
        `;
    } catch (error) {
        showError(result, error);
    }
}


async function generateQuiz() {
    const topic = document.getElementById("quizTopic").value.trim();
    const difficulty = document.getElementById("quizDifficulty").value;
    const result = document.getElementById("quizResult");

    if (!topic) {
        result.innerHTML = "Please enter a quiz topic.";
        return;
    }

    showLoading(result);

    try {
        const data = await sendRequest("/api/quiz", {
            topic: topic,
            difficulty: difficulty
        });

        let html = `
            <strong>${escapeHtml(data.topic)} Quiz</strong>
            <br><br>
        `;

        data.quiz.forEach((question, index) => {
            html += `
                <div class="quiz-question">
                    <strong>${index + 1}. ${escapeHtml(question.question)}</strong>
                    <br><br>
            `;

            question.options.forEach(option => {
                html += `
                    <div>• ${escapeHtml(option)}</div>
                `;
            });

            html += `
                    <br>
                    <strong>Answer:</strong>
                    ${escapeHtml(question.answer)}
                    <br>
                    <small>${escapeHtml(question.explanation || "")}</small>
                </div>
                <hr>
            `;
        });

        html += `
            <small>Source: ${escapeHtml(data.source || "EduGenie")}</small>
        `;

        result.innerHTML = html;

    } catch (error) {
        showError(result, error);
    }
}


async function getRecommendations() {
    const topic = document
        .getElementById("recommendationTopic")
        .value
        .trim();

    const result = document.getElementById("recommendationResult");

    showLoading(result);

    try {
        const response = await fetch(
            `/api/learn/recommendations?topic=${encodeURIComponent(topic)}`
        );

        if (!response.ok) {
            throw new Error(`Request failed: ${response.status}`);
        }

        const data = await response.json();

        let html = `
            <strong>Learning Plan</strong>
            <br><br>
        `;

        data.recommendations.forEach((item, index) => {
            html += `
                <div>
                    <strong>${index + 1}. ${escapeHtml(item.title)}</strong>
                    <br>
                    ${escapeHtml(item.description)}
                    <br>
                    <small>Action: ${escapeHtml(item.action)}</small>
                </div>
                <br>
            `;
        });

        html += `
            <small>Source: ${escapeHtml(data.source || "EduGenie")}</small>
        `;

        result.innerHTML = html;

    } catch (error) {
        showError(result, error);
    }
}


function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value ?? "";
    return div.innerHTML;
}


function formatText(value) {
    return escapeHtml(value).replace(/\n/g, "<br>");
}
