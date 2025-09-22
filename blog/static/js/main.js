// Wait for the HTML document to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', function () {
    // Select the hamburger menu toggle and the navigation links container
    const navToggle = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    // Add a click event listener to the toggle button
    navToggle.addEventListener('click', function () {
        // When clicked, toggle the 'active' class on the navigation links container
        navLinks.classList.toggle('active');
    });
});