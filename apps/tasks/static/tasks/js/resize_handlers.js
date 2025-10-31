document.addEventListener('DOMContentLoaded', () => {
    const horizontalResizer = document.getElementById('horizontal-resizer');
    const verticalResizer = document.getElementById('vertical-resizer');

    const problemSection = document.getElementById('problem-section');
    const rightPanel = document.querySelector('.right-panel');
    const editorSection = document.getElementById('editor-section');
    const outputResultsSection = document.getElementById('output-results-section');
    const editorOutputContainer = document.querySelector('.editor-output-container');

    let isHorizontalResizing = false;
    let isVerticalResizing = false;

    horizontalResizer?.addEventListener('mousedown', e => {
        isHorizontalResizing = true;
        document.body.classList.add('resizing');
        e.preventDefault();
    });

    verticalResizer?.addEventListener('mousedown', e => {
        isVerticalResizing = true;
        document.body.classList.add('resizing');
        e.preventDefault();
    });

    document.addEventListener('mousemove', e => {
        if (isHorizontalResizing) {
            const containerRect = document.querySelector('.main-container').getBoundingClientRect();
            const containerWidth = containerRect.width;
            const x = e.clientX - containerRect.left;

            const problemWidthPercent = (x / containerWidth) * 100;
            const rightPanelWidthPercent = 100 - problemWidthPercent;

            if (problemWidthPercent >= 20 && rightPanelWidthPercent >= 30) {
                problemSection.style.width = `${problemWidthPercent}%`;
                rightPanel.style.width = `${rightPanelWidthPercent}%`;
                editor?.layout();
            }
        }

        if (isVerticalResizing) {
            const containerRect = editorOutputContainer.getBoundingClientRect();
            const containerHeight = containerRect.height;
            const y = e.clientY - containerRect.top;

            const editorHeightPercent = (y / containerHeight) * 100;
            const outputHeightPercent = 100 - editorHeightPercent;

            if (editorHeightPercent >= 20 && outputHeightPercent >= 20) {
                editorSection.style.height = `${editorHeightPercent}%`;
                outputResultsSection.style.height = `${outputHeightPercent}%`;
                editor?.layout();
            }
        }
    });

    document.addEventListener('mouseup', () => {
        isHorizontalResizing = false;
        isVerticalResizing = false;
        document.body.classList.remove('resizing');
    });
});
