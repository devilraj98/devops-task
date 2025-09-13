const http = require('http');
const fs = require('fs');
const path = require('path');

console.log('Starting tests...');

// Test 1: Check if app.js file exists
function testAppFileExists() {
    const appPath = path.join(__dirname, 'app.js');
    if (fs.existsSync(appPath)) {
        console.log('✓ Test 1 PASSED: app.js file exists');
        return true;
    } else {
        console.log('✗ Test 1 FAILED: app.js file not found');
        return false;
    }
}

// Test 2: Check if logo file exists
function testLogoFileExists() {
    const logoPath = path.join(__dirname, 'logoswayatt.png');
    if (fs.existsSync(logoPath)) {
        console.log('✓ Test 2 PASSED: logoswayatt.png file exists');
        return true;
    } else {
        console.log('✗ Test 2 FAILED: logoswayatt.png file not found');
        return false;
    }
}

// Test 3: Check if package.json has required dependencies
function testPackageJson() {
    try {
        const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
        if (packageJson.dependencies && packageJson.dependencies.express) {
            console.log('✓ Test 3 PASSED: Express dependency found');
            return true;
        } else {
            console.log('✗ Test 3 FAILED: Express dependency not found');
            return false;
        }
    } catch (error) {
        console.log('✗ Test 3 FAILED: Error reading package.json');
        return false;
    }
}

// Run all tests
function runTests() {
    const test1 = testAppFileExists();
    const test2 = testLogoFileExists();
    const test3 = testPackageJson();
    
    const totalTests = 3;
    const passedTests = [test1, test2, test3].filter(Boolean).length;
    
    console.log(`\nTest Results: ${passedTests}/${totalTests} tests passed`);
    
    if (passedTests === totalTests) {
        console.log('🎉 All tests passed!');
        process.exit(0);
    } else {
        console.log('❌ Some tests failed!');
        process.exit(1);
    }
}

runTests();