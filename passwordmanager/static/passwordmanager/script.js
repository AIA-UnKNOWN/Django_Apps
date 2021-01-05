(function() {
  const logoutButton = document.querySelector('#logout');
  logoutButton.addEventListener('click', function(e) {
    location.href = e.target.value;
  })
})();