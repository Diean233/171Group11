(function() {

    'use strict';
    console.log("reading js");

    const navItems = document.querySelectorAll('nav ul:first-child li');
    const navLinks = document.querySelectorAll('nav ul:first-child li a');
    
    navItems.forEach(function(item, i) {
        item.addEventListener("click", function(e) {
            e.preventDefault();
            let targetID = navLinks[i].getAttribute('href');
            let targetAnchor = document.getElementById(targetID);
            let originalTop = Math.floor(targetAnchor.getBoundingClientRect().top) - 70;
            window.scrollBy({ top: originalTop, left: 0, behavior: 'smooth' });
        });
    });

    const backToTopButton = document.querySelector('#group-info');
    backToTopButton.addEventListener("click", function() {
        let targetAnchor = document.getElementById("#intro");
        let originalTop = Math.floor(targetAnchor.getBoundingClientRect().top) - 70;
        window.scrollBy({ top: originalTop, left: 0, behavior: 'smooth' });
    })

    const githubLink = document.querySelector('nav ul:last-child li');
    githubLink.addEventListener("click", function() {
        window.open("https://github.com/Diean233/171Group11");
    });
})();

