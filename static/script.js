// Global variables to track typing behavior
let keystrokeData = {
    timestamps: [],
    keyCount: 0,
    backspaceCount: 0,
    startTime: null,
    lastKeyTime: null,
    pauses: []
};

// Get DOM elements
const typingBox = document.getElementById('typing-box');
const charCount = document.getElementById('char-count');
const typingSpeed = document.getElementById('typing-speed');
const backspaceCount = document.getElementById('backspace-count');
const analyzeBtn = document.getElementById('analyze-btn');
const resultsSection = document.getElementById('results-section');

// Initialize event listeners
typingBox.addEventListener('keydown', handleKeyPress);
typingBox.addEventListener('input', updateStats);

/**
 * Handle each keypress to collect timing data
 */
function handleKeyPress(event) {
    const currentTime = Date.now();
    
    // Initialize start time on first keypress
    if (!keystrokeData.startTime) {
        keystrokeData.startTime = currentTime;
        keystrokeData.lastKeyTime = currentTime;
        return;
    }
    
    // Calculate pause duration since last key
    const pauseDuration = currentTime - keystrokeData.lastKeyTime;
    keystrokeData.pauses.push(pauseDuration);
    
    // Track backspace key
    if (event.key === 'Backspace') {
        keystrokeData.backspaceCount++;
    }
    
    // Update counters
    keystrokeData.keyCount++;
    keystrokeData.timestamps.push(currentTime);
    keystrokeData.lastKeyTime = currentTime;
}

/**
 * Update real-time statistics display
 */
function updateStats() {
    const text = typingBox.value;
    charCount.textContent = text.length;
    backspaceCount.textContent = keystrokeData.backspaceCount;
    
    // Calculate typing speed
    if (keystrokeData.startTime && keystrokeData.keyCount > 0) {
        const elapsedSeconds = (Date.now() - keystrokeData.startTime) / 1000;
        const speed = keystrokeData.keyCount / elapsedSeconds;
        typingSpeed.textContent = speed.toFixed(2);
    }
    
    // Enable analyze button if enough text is typed
    if (text.length >= 50) {
        analyzeBtn.disabled = false;
        analyzeBtn.style.opacity = '1';
    } else {
        analyzeBtn.disabled = true;
        analyzeBtn.style.opacity = '0.6';
    }
}

/**
 * Calculate typing features and send to backend
 */
async function analyzeStress() {
    const text = typingBox.value;
    
    // Validate input
    if (text.length < 50) {
        alert('Please type at least 50 characters for accurate analysis.');
        return;
    }
    
    if (keystrokeData.keyCount === 0) {
        alert('No typing data collected. Please try typing again.');
        return;
    }
    
    // Show loading state
    analyzeBtn.textContent = '🔄 Analyzing...';
    analyzeBtn.disabled = true;
    
    try {
        // Calculate features
        const features = calculateFeatures();
        
        // Send to backend
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(features)
        });
        
        if (!response.ok) {
            throw new Error('Analysis failed. Please try again.');
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        alert('Error: ' + error.message);
        analyzeBtn.textContent = '🔍 Analyze Stress Level';
        analyzeBtn.disabled = false;
    }
}

/**
 * Calculate typing behavior features
 */
function calculateFeatures() {
    const totalTime = (Date.now() - keystrokeData.startTime) / 1000; // in seconds
    
    // Typing speed (keys per second)
    const typingSpeed = keystrokeData.keyCount / totalTime;
    
    // Average pause duration (in milliseconds)
    let avgPause = 0;
    if (keystrokeData.pauses.length > 0) {
        const totalPause = keystrokeData.pauses.reduce((sum, pause) => sum + pause, 0);
        avgPause = totalPause / keystrokeData.pauses.length;
    }
    
    // Error rate (backspaces per total keys)
    const errorRate = keystrokeData.backspaceCount / keystrokeData.keyCount;
    
    return {
        typing_speed: typingSpeed,
        avg_pause: avgPause,
        error_rate: errorRate
    };
}

/**
 * Display prediction results
 */
function displayResults(result) {
    // Hide typing section and show results
    typingBox.disabled = true;
    analyzeBtn.style.display = 'none';
    resultsSection.classList.remove('hidden');
    
    // Display stress level with color coding
    const stressLevel = document.getElementById('stress-level');
    stressLevel.textContent = result.stress_level;
    stressLevel.className = 'value stress-' + result.stress_level.toLowerCase();
    
    // Display confidence
    document.getElementById('confidence').textContent = result.confidence + '%';
    
    // Display features with visualization
    displayFeatureBar('speed', result.features.typing_speed, 5, result.features.typing_speed + ' keys/sec');
    displayFeatureBar('pause', result.features.avg_pause, 2000, result.features.avg_pause + ' ms');
    displayFeatureBar('error', result.features.error_rate, 50, result.features.error_rate + '%');
    
    // Display tips
    const tipsList = document.getElementById('tips-list');
    tipsList.innerHTML = '';
    result.tips.forEach(tip => {
        const li = document.createElement('li');
        li.textContent = tip;
        tipsList.appendChild(li);
    });
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Display feature as a bar chart
 */
function displayFeatureBar(featureName, value, maxValue, displayText) {
    const bar = document.getElementById(featureName + '-bar');
    const valueSpan = document.getElementById(featureName + '-value');
    
    const percentage = Math.min((value / maxValue) * 100, 100);
    bar.style.width = percentage + '%';
    
    // Color code based on value
    if (percentage < 33) {
        bar.style.backgroundColor = '#4CAF50';
    } else if (percentage < 66) {
        bar.style.backgroundColor = '#FFC107';
    } else {
        bar.style.backgroundColor = '#F44336';
    }
    
    valueSpan.textContent = displayText;
}

/**
 * Reset the app for a new analysis
 */
function resetApp() {
    // Reset data
    keystrokeData = {
        timestamps: [],
        keyCount: 0,
        backspaceCount: 0,
        startTime: null,
        lastKeyTime: null,
        pauses: []
    };
    
    // Reset UI
    typingBox.value = '';
    typingBox.disabled = false;
    charCount.textContent = '0';
    typingSpeed.textContent = '0';
    backspaceCount.textContent = '0';
    
    analyzeBtn.textContent = '🔍 Analyze Stress Level';
    analyzeBtn.style.display = 'block';
    analyzeBtn.disabled = true;
    
    resultsSection.classList.add('hidden');
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Focus on text box
    typingBox.focus();
}
