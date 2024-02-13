// <!-- Script for handling Login form submission and Invalid Credentials displaying SweetAlert pop-ups -->

  document.querySelector('.login-form form').addEventListener('submit', function(e) {
      e.preventDefault(); // Prevent the default form submission

      const formData = new FormData(this);
      const actionUrl = this.getAttribute('action');

      fetch(actionUrl, {
          method: 'POST',
          body: formData
      })
      .then(response => {
          if (!response.ok) {
              // Check for specific HTTP status code 401
              if (response.status === 401) {
                  // Throw an error for 401 Unauthorized
                  throw new Error('Invalid Credentials');
              } else {
                  // Throw an error for other HTTP error responses
                  throw new Error('HTTP error, status = ' + response.status);
              }
          }
          return response.json();
      })
      .then(data => {
          if (data.error) {
              // Display a SweetAlert for invalid credentials
              Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: data.error
              });
          } else if (data.success) {
              // Display a SweetAlert for successful login
              Swal.fire({
                  icon: 'success',
                  title: 'Success!',
                  text: data.success,
                  timer: 2000,  // Set a timer to automatically close the alert after 2 seconds
                  showConfirmButton: false
              }).then(() => {
                  window.location.href = '/id'; // Redirect to ID page
              });
          }
      })
      .catch(error => {
          // Check if the error message is 'Invalid Credentials' (for 401 error)
          if (error.message === 'Invalid Credentials') {
              // Display a SweetAlert for 401 Unauthorized
              Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Invalid Credentials!'
              });
          } else {
              // Display a SweetAlert for generic error
              Swal.fire({
                  icon: 'error',
                  title: 'Oops...',
                  text: 'Something went wrong!'
              });
          }
      });
  });
