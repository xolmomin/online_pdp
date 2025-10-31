document.addEventListener("DOMContentLoaded", () => {
    const runButton = document.querySelector(".run-button");
    const submitButton = document.querySelector(".submit-button");
    const outputBox = document.getElementById("output-box");
    const testResults = document.getElementById("test-results");
    const resultsSummary = document.getElementById("results-summary");

    const runUrl = window.urls.runCode;
    const submitUrl = window.urls.submitCode;
    const problemId = window.problemID;


    runButton.addEventListener("click", () => sendCode(runUrl));
    submitButton.addEventListener("click", () => sendCode(submitUrl, true));

    async function sendCode(url, includeProblem = false) {
        const code = editor.getValue().trim();
        const body = includeProblem ? {code, problem_id: problemId} : {code};

        outputBox.textContent = "Running...";
        testResults.innerHTML = '<div class="text-gray-500 text-sm p-4 text-center">Running tests...</div>';
        resultsSummary.style.display = 'none';

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(body)
            });

            const data = await response.json();
            outputBox.textContent = data.output || "No output returned.";

            if (Array.isArray(data.results)) {
                displayTestResults(data.results);
            }
        } catch (error) {
            outputBox.textContent = "Error running code: " + error;
        }
    }

    function displayTestResults(results) {
        testResults.innerHTML = '';
        let passed = 0, failed = 0;

        results.forEach(result => {
            const el = document.createElement('div');
            el.className = 'test-case';
            const statusClass = result.verdict === "AC" ? 'status-passed' : 'status-failed';
            const statusText = result.verdict === "AC" ? 'Passed' : result.verdict;

            el.innerHTML = `
                <div class="test-case-header">
                    <div class="test-case-title">Test Case #${result.testcase}</div>
                    <div class="test-case-status ${statusClass}">${statusText}</div>
                </div>
                <div class="test-case-details">
                    <div class="test-input"><span>Input:</span> ${result.input}</div>
                    <div class="test-expected"><span>Expected:</span> ${result.expected}</div>
                    <div class="test-actual"><span>Output:</span> ${result.actual || result.stdout || 'No output'}</div>
                </div>
            `;

            testResults.appendChild(el);
            if (result.verdict === "AC") passed++; else failed++;
        });

        document.getElementById('passed-count').textContent = passed;
        document.getElementById('failed-count').textContent = failed;
        document.getElementById('total-count').textContent = results.length;

        const summaryMessage = document.getElementById('summary-message');
        if (passed === results.length) {
            summaryMessage.textContent = '🎉 All test cases passed!';
            summaryMessage.className = 'summary-message message-passed';
        } else {
            summaryMessage.textContent = '❌ Some test cases failed';
            summaryMessage.className = 'summary-message message-failed';
        }

        resultsSummary.style.display = 'block';
    }

    function getCookie(name) {
        let cookieValue = null;
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
        return cookieValue;
    }
});
