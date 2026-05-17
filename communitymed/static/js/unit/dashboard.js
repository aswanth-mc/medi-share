const sidebar = document.querySelector(".sidebar");
const overlay = document.querySelector(".sidebar-overlay");

function toggleSidebar() {
    sidebar.classList.toggle("active");
    overlay.classList.toggle("active");
}

// Close sidebar when clicking overlay
overlay.addEventListener("click", () => {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
});

// Close sidebar on resize if desktop
window.addEventListener("resize", () => {
    if (window.innerWidth > 768) {
        sidebar.classList.remove("active");
        overlay.classList.remove("active");
    }
});


// Chart.js example for donation trends
const ctx = document.getElementById("donationChart");

if (ctx) {
    new Chart(ctx, {
        type: "bar",

        data: {
            labels: [
                "Mon",
                "Tue",
                "Wed",
                "Thu",
                "Fri",
                "Sat",
                "Sun"
            ],

            datasets: [{
                label: "Medicine Donations",

                data: [12, 19, 8, 15, 22, 18, 25],

                borderWidth: 1,

                borderRadius: 10
            }]
        },

        options: {
            responsive: true,

            maintainAspectRatio: false,

            plugins: {
                legend: {
                    display: false
                }
            },

            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}