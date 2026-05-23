const chartElement = document.getElementById("donationChart");

if (chartElement && window.Chart) {
  new Chart(chartElement, {
    type: "bar",
    data: {
      labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
      datasets: [
        {
          label: "Approved",
          data: [12, 18, 14, 22, 25, 30],
          backgroundColor: "#2d9cdb",
          borderRadius: 8
        },
        {
          label: "Pending",
          data: [4, 6, 3, 8, 5, 7],
          backgroundColor: "#f2994a",
          borderRadius: 8
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          labels: {
            boxWidth: 12,
            color: "#6b7280"
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          }
        },
        y: {
          beginAtZero: true,
          ticks: {
            precision: 0
          }
        }
      }
    }
  });
}