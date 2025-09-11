document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav-menu a');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-menu a');
  const sections = document.querySelectorAll('.page-section');

  window.addEventListener('scroll', function() {
    let current = '';
    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      if (pageYOffset >= (sectionTop - 100)) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href').includes(current)) {
        link.classList.add('active');
      }
    });

    mobileNavLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href').includes(current)) {
        link.classList.add('active');
      }
    });

    const scrollToTopBtn = document.getElementById('scrollToTop');
    if (scrollToTopBtn) {
      if (window.pageYOffset > 300) {
        scrollToTopBtn.classList.add('show');
      } else {
        scrollToTopBtn.classList.remove('show');
      }
    }
  });

  const scrollToTopBtn = document.getElementById('scrollToTop');
  if (scrollToTopBtn) {
    scrollToTopBtn.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const closeMobileMenu = document.getElementById('closeMobileMenu');
  const mobileNavOverlay = document.getElementById('mobileNavOverlay');
  const mobileNavMenu = document.getElementById('mobileNavMenu');

  function openMobileMenu() {
    mobileNavOverlay.classList.add('active');
    mobileNavMenu.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenuFunc() {
    mobileNavOverlay.classList.remove('active');
    mobileNavMenu.classList.remove('active');
    document.body.style.overflow = 'auto';
  }

  if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', openMobileMenu);
  if (closeMobileMenu) closeMobileMenu.addEventListener('click', closeMobileMenuFunc);
  if (mobileNavOverlay) mobileNavOverlay.addEventListener('click', closeMobileMenuFunc);

  mobileNavLinks.forEach(link => {
    link.addEventListener('click', closeMobileMenuFunc);
  });

  const toggleSidebar = document.getElementById('toggleSidebar');
  const sidebar = document.getElementById('sidebar');

  if (toggleSidebar) {
    toggleSidebar.addEventListener('click', function() {
      sidebar.classList.toggle('active');
    });
  }

  document.addEventListener('click', function(event) {
    if (sidebar && sidebar.classList.contains('active') &&
        !sidebar.contains(event.target) &&
        !toggleSidebar.contains(event.target)) {
      sidebar.classList.remove('active');
    }
  });
});
