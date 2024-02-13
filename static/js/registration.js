// <!-- Script for handling  Registration form submission and displaying SweetAlert pop-ups for Phone number exists -->

  document.querySelector('.signup-form form').addEventListener('submit', function(e) {
      e.preventDefault(); // Prevent the default form submission

      const formData = new FormData(this);
      const actionUrl = this.getAttribute('action');

      fetch(actionUrl, {
          method: 'POST',
          body: formData
      })
      .then(response => {
          if (!response.ok) throw new Error('Network response was not ok.');
          return response.json();
      })
      .then(data => {
          if (data.error) {
              // Display a SweetAlert for error message
              Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: data.error
              });
          } else if (data.success) {
              // Display a SweetAlert for successful registration
              Swal.fire({
                  icon: 'success',
                  title: 'Registration Successful',
                  text: 'You have successfully registered.',
                  timer: 2000,  // Set a timer to automatically close the alert after 2 seconds
                  showConfirmButton: false
              }).then(() => {
                  window.location.href = '/id'; // Redirect to ID page
              });
          }
      })
      .catch(error => {
          console.error('Error:', error);
          // Display a SweetAlert for generic error
          Swal.fire({
              icon: 'error',
              title: 'Oops...',
              text: 'Phone Number Already Exists Please Login!'
          });
      });
  });
