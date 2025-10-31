document.addEventListener("DOMContentLoaded", function () {
    require.config({
        paths: {'vs': 'https://cdn.jsdelivr.net/npm/monaco-editor@0.49.0/min/vs'}
    });

    require(['vs/editor/editor.main'], function () {
        // Define custom theme with enhanced syntax highlighting
        monaco.editor.defineTheme('enhancedLight', {
            base: 'vs',
            inherit: true,
            rules: [
                { token: 'keyword', foreground: '7c3aed', fontStyle: 'bold' },
                { token: 'string', foreground: '059669' },
                { token: 'number', foreground: 'dc2626', fontStyle: 'bold' },
                { token: 'comment', foreground: '6b7280', fontStyle: 'italic' },
                { token: 'function', foreground: '2563eb', fontStyle: 'bold' },
                { token: 'variable', foreground: '0f172a' },
                { token: 'type', foreground: '0891b2', fontStyle: 'bold' },
                { token: 'class', foreground: 'd97706', fontStyle: 'bold' },
                { token: 'operator', foreground: '475569' },
            ],
            colors: {
                'editor.background': '#ffffff',
                'editor.foreground': '#0f172a',
                'editor.lineHighlightBackground': '#f1f5f9',
                'editor.selectionBackground': '#bfdbfe',
                'editor.inactiveSelectionBackground': '#e0e7ff',
                'editorCursor.foreground': '#3b82f6',
                'editorLineNumber.foreground': '#94a3b8',
                'editorLineNumber.activeForeground': '#3b82f6',
            }
        });

        window.editor = monaco.editor.create(document.getElementById('python-editor'), {
            value: `# Write your Python code here\n`,
            language: "python",
            theme: "enhancedLight",
            automaticLayout: true,
            minimap: { enabled: false },
            fontSize: 15,
            letterSpacing: 0.5,
            scrollBeyondLastLine: false,
            wordWrap: "on",
            insertSpaces: true,
            tabSize: 4,
            detectIndentation: false,
            fontFamily: "'Fira Code', 'JetBrains Mono', 'Consolas', 'Monaco', monospace",
            renderWhitespace: 'boundary',
            renderIndentGuides: true,
            fontLigatures: true,
            smoothScrolling: true,
            cursorSmoothCaretAnimation: 'on',

            // Enhanced Line Numbers
            lineNumbers: "on",
            glyphMargin: true,
            folding: true,
            lineDecorationsWidth: 10,
            lineNumbersMinChars: 4,

            // Code Formatting
            formatOnPaste: true,
            formatOnType: true,

            // Enhanced Suggestions & IntelliSense
            quickSuggestions: {
                other: true,
                comments: false,
                strings: true
            },
            suggestOnTriggerCharacters: true,
            acceptSuggestionOnEnter: "on",
            snippetSuggestions: 'top',
            wordBasedSuggestions: 'matchingDocuments',

            // Visual Enhancements
            cursorBlinking: "smooth",
            cursorStyle: "line",
            cursorWidth: 3,
            roundedSelection: true,
            selectionHighlight: true,
            occurrencesHighlight: 'multiFile',
            bracketPairColorization: {
                enabled: true
            },

            // Editor Padding
            padding: { top: 20, bottom: 20 },

            // Scrollbar
            scrollbar: {
                verticalScrollbarSize: 12,
                horizontalScrollbarSize: 12,
                useShadows: true
            }
        });

        // Store decorations
        window.decorations = [];
        window.errorDecorations = [];

        // ==================== PYTHON KEYWORDS ====================
        const pythonKeywords = [
            'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'return',
            'import', 'from', 'as', 'try', 'except', 'finally', 'with',
            'lambda', 'yield', 'pass', 'break', 'continue', 'and', 'or',
            'not', 'in', 'is', 'None', 'True', 'False', 'raise', 'assert'
        ];

        // ==================== BUILT-IN FUNCTIONS ====================
        const builtInFunctions = [
            'print', 'len', 'range', 'enumerate', 'zip', 'map', 'filter',
            'sorted', 'sum', 'max', 'min', 'abs', 'round', 'type', 'str',
            'int', 'float', 'bool', 'list', 'dict', 'set', 'tuple',
            'open', 'input', 'format', 'isinstance', 'hasattr', 'getattr'
        ];

        // ==================== SYNTAX ERROR DETECTION ====================
        function detectSyntaxErrors() {
            const model = window.editor.getModel();
            const content = model.getValue();
            const lines = content.split('\n');
            const newErrorDecorations = [];

            lines.forEach((line, index) => {
                const lineNumber = index + 1;
                const trimmedLine = line.trim();

                // Skip empty lines and comments
                if (!trimmedLine || trimmedLine.startsWith('#')) return;

                // Check for unclosed strings
                const singleQuotes = (line.match(/'/g) || []).length;
                const doubleQuotes = (line.match(/"/g) || []).length;
                const escapedSingleQuotes = (line.match(/\\'/g) || []).length;
                const escapedDoubleQuotes = (line.match(/\\"/g) || []).length;

                if ((singleQuotes - escapedSingleQuotes) % 2 !== 0 ||
                    (doubleQuotes - escapedDoubleQuotes) % 2 !== 0) {
                    newErrorDecorations.push({
                        range: new monaco.Range(lineNumber, 1, lineNumber, line.length + 1),
                        options: {
                            isWholeLine: true,
                            className: 'syntax-error-decoration',
                            glyphMarginClassName: 'syntax-error-glyph',
                            hoverMessage: { value: '⚠️ **Syntax Error**: Unclosed string' }
                        }
                    });
                }

                // Check for unmatched brackets/parentheses
                const openBrackets = (line.match(/[\[\(\{]/g) || []).length;
                const closeBrackets = (line.match(/[\]\)\}]/g) || []).length;

                // Check for common indentation errors
                if (trimmedLine.match(/^(def|class|if|else|elif|for|while|try|except|finally|with)\b/) &&
                    !trimmedLine.endsWith(':')) {
                    newErrorDecorations.push({
                        range: new monaco.Range(lineNumber, 1, lineNumber, line.length + 1),
                        options: {
                            isWholeLine: true,
                            className: 'syntax-error-decoration',
                            glyphMarginClassName: 'syntax-error-glyph',
                            hoverMessage: { value: '⚠️ **Syntax Error**: Missing colon (:) at end of statement' }
                        }
                    });
                }

                // Check for invalid variable names starting with numbers
                const varMatch = trimmedLine.match(/^\s*(\d+\w+)\s*=/);
                if (varMatch) {
                    const startCol = line.indexOf(varMatch[1]) + 1;
                    newErrorDecorations.push({
                        range: new monaco.Range(lineNumber, startCol, lineNumber, startCol + varMatch[1].length),
                        options: {
                            className: 'syntax-error-decoration',
                            glyphMarginClassName: 'syntax-error-glyph',
                            hoverMessage: { value: '⚠️ **Syntax Error**: Variable name cannot start with a number' }
                        }
                    });
                }
            });

            // Apply error decorations
            window.errorDecorations = window.editor.deltaDecorations(
                window.errorDecorations,
                newErrorDecorations
            );
        }

        // ==================== BUILT-IN FUNCTION DETECTION ====================
        function detectBuiltInFunctions() {
            const model = window.editor.getModel();
            const content = model.getValue();
            const newDecorations = [];

            builtInFunctions.forEach(func => {
                const regex = new RegExp(`\\b${func}\\b(?=\\s*\\()`, 'g');
                let match;

                while ((match = regex.exec(content)) !== null) {
                    const startPos = model.getPositionAt(match.index);
                    const endPos = model.getPositionAt(match.index + func.length);

                    newDecorations.push({
                        range: new monaco.Range(
                            startPos.lineNumber,
                            startPos.column,
                            endPos.lineNumber,
                            endPos.column
                        ),
                        options: {
                            inlineClassName: 'builtin-function-inline',
                            glyphMarginClassName: 'builtin-function-glyph',
                            hoverMessage: {
                                value: `**${func}()** - Built-in Python function\n\n${getFunctionDescription(func)}`
                            }
                        }
                    });
                }
            });

            // Apply decorations
            window.decorations = window.editor.deltaDecorations(
                window.decorations,
                newDecorations
            );
        }

        // ==================== FUNCTION DESCRIPTIONS ====================
        function getFunctionDescription(funcName) {
            const descriptions = {
                'print': 'Prints objects to the text stream',
                'len': 'Returns the length (number of items) of an object',
                'range': 'Generates a sequence of numbers',
                'enumerate': 'Returns an enumerate object with index-value pairs',
                'zip': 'Creates an iterator of tuples from multiple iterables',
                'map': 'Applies a function to all items in an iterable',
                'filter': 'Filters items based on a function that returns True/False',
                'sorted': 'Returns a sorted list from the items in an iterable',
                'sum': 'Sums all items in an iterable',
                'max': 'Returns the largest item',
                'min': 'Returns the smallest item',
                'abs': 'Returns the absolute value of a number',
                'round': 'Rounds a number to a specified precision',
                'type': 'Returns the type of an object',
                'str': 'Converts an object to a string',
                'int': 'Converts to an integer',
                'float': 'Converts to a floating point number',
                'bool': 'Converts to a boolean',
                'list': 'Creates a list object',
                'dict': 'Creates a dictionary object',
                'set': 'Creates a set object',
                'tuple': 'Creates a tuple object',
                'open': 'Opens a file and returns a file object',
                'input': 'Reads a line from input',
                'format': 'Formats a specified value',
                'isinstance': 'Checks if an object is an instance of a class',
                'hasattr': 'Checks if an object has a specific attribute',
                'getattr': 'Gets the value of a named attribute'
            };
            return descriptions[funcName] || 'Python built-in function';
        }

        // ==================== CONTENT CHANGE MONITORING ====================
        window.editor.onDidChangeModelContent(function () {
            detectBuiltInFunctions();
            detectSyntaxErrors();
        });

        // ==================== AUTO-COMPLETE FOR BUILT-IN FUNCTIONS ====================
        monaco.languages.registerCompletionItemProvider('python', {
            provideCompletionItems: function (model, position) {
                const word = model.getWordUntilPosition(position);
                const range = {
                    startLineNumber: position.lineNumber,
                    startColumn: word.startColumn,
                    endLineNumber: position.lineNumber,
                    endColumn: word.endColumn
                };

                const suggestions = builtInFunctions.map(func => ({
                    label: func,
                    kind: monaco.languages.CompletionItemKind.Function,
                    documentation: getFunctionDescription(func),
                    insertText: `${func}($1)`,
                    insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
                    range: range,
                    detail: 'Built-in function'
                }));

                // Add keyword completions
                const keywordSuggestions = pythonKeywords.map(keyword => ({
                    label: keyword,
                    kind: monaco.languages.CompletionItemKind.Keyword,
                    insertText: keyword,
                    range: range,
                    detail: 'Python keyword'
                }));

                return { suggestions: [...suggestions, ...keywordSuggestions] };
            }
        });

        // ==================== KEYBOARD SHORTCUTS ====================

        // Ctrl+Enter or Cmd+Enter to run code
        window.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, function () {
            const runButton = document.querySelector('.run-button');
            if (runButton) {
                runButton.click();
            }
        });

        // Ctrl+/ or Cmd+/ to toggle comment
        window.editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Slash, function () {
            window.editor.trigger('keyboard', 'editor.action.commentLine');
        });

        // Detect on initial load
        detectBuiltInFunctions();
        detectSyntaxErrors();

        // Add status indicator
        console.log('✅ Monaco Editor initialized with enhanced syntax highlighting and error detection');
    });
});