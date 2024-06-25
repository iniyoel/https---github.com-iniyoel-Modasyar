function submitForm() {
    var firstName = document.getElementById("firstName").value;
    var lastName = document.getElementById("lastName").value;
    var userName = document.getElementById("userName").value;
    var phoneNumber = document.getElementById("phoneNumber").value;
    var birthDate = document.getElementById("birthDate").value;

    var userDetails = {
        firstName: firstName,
        lastName: lastName,
        userName: userName,
        phoneNumber: phoneNumber,
        birthDate: birthDate
    };

    // Simpan userDetails ke localStorage
    localStorage.setItem('userDetails', JSON.stringify(userDetails));

    // Contoh: Tautan ke halaman profil pengguna
    window.location.href = "{% url 'userdashboard'%}";
}

document.addEventListener('DOMContentLoaded', function() {
    var userDetails = localStorage.getItem('userDetails');
    if (userDetails) {
        userDetails = JSON.parse(userDetails);
        var userNameElement = document.getElementById('userName');
        if (userNameElement) {
            userNameElement.textContent = userDetails.userName;
        }
        // Anda juga bisa menampilkan detail lainnya seperti berikut:
        document.getElementById('firstName').textContent = userDetails.firstName;
        document.getElementById('lastName').textContent = userDetails.lastName;
        document.getElementById('phoneNumber').textContent = userDetails.phoneNumber;
        document.getElementById('birthDate').textContent = userDetails.birthDate;
    }
});


// Ambil query string dari URL
var queryString = window.location.search;
var urlParams = new URLSearchParams(queryString);

// Ambil nilai dari setiap parameter query string
var firstName = urlParams.get('firstName');
var lastName = urlParams.get('lastName');
var userName = urlParams.get('userName');
var phoneNumber = urlParams.get('phoneNumber');
var birthDate = urlParams.get('birthDate');

// Ubah format tanggal lahir menjadi "dd/mm/yyyy"
var formattedBirthDate = new Date(birthDate).toLocaleDateString('en-GB');
document.getElementById("birthDate").innerHTML = "<strong>Tanggal Lahir:</strong><br> " + formattedBirthDate;

// Tampilkan detail pengguna di dalam elemen HTML
document.getElementById("firstName").innerHTML = firstName;
document.getElementById("lastName").innerHTML = lastName;
document.getElementById("userName").innerHTML = userName;
document.getElementById("phoneNumber").innerHTML = "<strong>Nomor Telepon:</strong><br> " + phoneNumber;
