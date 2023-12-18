document.addEventListener("DOMContentLoaded", function() {
    const searchIcon = document.getElementById("searchIcon");
    const searchInput = document.getElementById("searchInput");
  
    searchIcon.addEventListener("click", function() {
      searchInput.focus();
    });
  });
  