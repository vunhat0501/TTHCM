const questionText = document.getElementById("question-text");
const optionsContainer = document.getElementById("options-container");
const nextBtn = document.getElementById("next-btn");
const quizContainer = document.getElementById("quiz-container");
const resultContainer = document.getElementById("result-container");
const scoreText = document.getElementById("score-text");
const restartBtn = document.getElementById("restart-btn");

let currentQuestionIndex = 0;
let score = 0;
let quizData = [];

// Fetch data from JSON file
async function loadQuizData() {
    try {
        const response = await fetch("data.json");
        quizData = await response.json();
        startQuiz();
    } catch (error) {
        questionText.innerText =
            "Lỗi khi tải dữ liệu câu hỏi. Vui lòng kiểm tra lại server.";
        console.error("Error loading JSON:", error);
    }
}

function startQuiz() {
    currentQuestionIndex = 0;
    score = 0;
    quizContainer.classList.remove("hidden");
    resultContainer.classList.add("hidden");
    showQuestion();
}

function showQuestion() {
    resetState();
    const currentQuestion = quizData[currentQuestionIndex];
    questionText.innerText = currentQuestion.question;

    currentQuestion.options.forEach((option, index) => {
        const button = document.createElement("button");
        button.innerText = option;
        button.classList.add("option-btn");
        button.dataset.index = index;
        button.addEventListener("click", selectAnswer);
        optionsContainer.appendChild(button);
    });
}

function resetState() {
    nextBtn.classList.add("hidden");
    while (optionsContainer.firstChild) {
        optionsContainer.removeChild(optionsContainer.firstChild);
    }
}

function selectAnswer(e) {
    const selectedBtn = e.target;
    const selectedIndex = parseInt(selectedBtn.dataset.index);
    const correctIndex = quizData[currentQuestionIndex].answer;

    const isCorrect = selectedIndex === correctIndex;

    if (isCorrect) {
        selectedBtn.classList.add("correct");
        score++;
    } else {
        selectedBtn.classList.add("wrong");
        // Highlight the correct answer
        const allOptions = optionsContainer.children;
        allOptions[correctIndex].classList.add("correct");
    }

    // Disable all buttons after selection
    Array.from(optionsContainer.children).forEach((button) => {
        button.disabled = true;
    });

    nextBtn.classList.remove("hidden");
}

nextBtn.addEventListener("click", () => {
    currentQuestionIndex++;
    if (currentQuestionIndex < quizData.length) {
        showQuestion();
    } else {
        showResult();
    }
});

function showResult() {
    quizContainer.classList.add("hidden");
    resultContainer.classList.remove("hidden");
    scoreText.innerText = `Bạn đã trả lời đúng ${score} / ${quizData.length} câu.`;
}

restartBtn.addEventListener("click", startQuiz);

// Initialize
loadQuizData();
