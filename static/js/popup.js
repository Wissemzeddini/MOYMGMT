document.getElementById('modal').style.display = 'block'
window.addEventListener('scroll', function(e) {
    setTimeout( () => {
      document.getElementById('modal').style.display = 'block'
    }, 2000 )
  });
  let modalAlreadyShowed = false

  window.addEventListener('scroll', function(e) {
    if( ! modalAlreadyShowed ) {
      setTimeout( () => {
        document.getElementById('modal').style.display = 'block'
      }, 2000 )
      modalAlreadyShowed = true
    }
  });
  document.getElementById('modal-close').addEventListener('click', function(e) {
    document.getElementById('modal').style.display = 'none'
  })