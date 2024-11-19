<template>
  <NavBar />
  <div class="container">

  <div class="row" style="margin-top: 80px;">
    <div class="col-sm-6">
    <canvas id="summaryGraph"></canvas>
    </div>
    <div class="col-sm-6">
    <canvas style="height: 50%; width:50%" id="ratingsDoughnutChart"></canvas>
    </div>
  </div>
  <button v-if="this.user && this.user.role == 'admin'" @click="generateCSVReport" class="btn btn-dark mt-4">Download Report as CSV</button>
</div>
</template>

<script>
import UserMixin from '../mixins/userMixin';
import NavBar from '../components/NavBar.vue';

export default {
  name: 'SummaryGraphs',
  mixins: [UserMixin],
  components: {
    NavBar,
  },
  data() {
    return {
      chartTitle: 'Service Requests Summary',
      chartInstance: null,
    };
  },
  created() {
    this.fetchDataAndRenderChart();
  },
  methods: {
    async fetchDataAndRenderChart() {
      try {
        const response = await fetch('http://127.0.0.1:5000/request_summary', { 
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
          },
        });
        const data = await response.json();
        const labels = Object.keys(data);
        const values = Object.values(data);

        this.renderChart(labels, values);


      // Fetch ratings data
      const ratingsResponse = await fetch('http://127.0.0.1:5000/ratings_summary', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
      });
      const ratingsData = await ratingsResponse.json();      

      const ratingsLabels = Object.keys(ratingsData).map(rating =>
        rating === "Not Rated Yet" ? "Not Rated Yet" : `${rating} Stars`
      );
      const ratingsValues = Object.values(ratingsData);
      
      const totalRatings = ratingsValues.reduce((sum, count) => sum + count, 0);
      if(totalRatings!=0){
      this.renderRatingsChart(ratingsLabels, ratingsValues, totalRatings);
    }

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },

    renderChart(labels, values) {
      const ctx = document.getElementById('summaryGraph').getContext('2d');
      
      // Destroy old chart instance if it exists
      if (this.chartInstance) this.chartInstance.destroy();

      const maxValue = Math.max(...values);
      const adjustedMax = Math.ceil(maxValue / 2) * 2;

      // Create new chart instance
      this.chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [
            {
              label: 'Number of Requests',
              data: values,
              backgroundColor: ['#4BC0C0', '#FF9F40', '#9966FF', '#FF6384'],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false, // Hide the legend entirely
            },
            title: {
              display: true,
              text: this.chartTitle,
            },
          },
          scales: {
            x:{
              title: {
                display: true,
                text: 'Status',
              }
            },
            y: {
              title: {
                display: true,
                text: 'Count',
              },
              min: 0,
              max: adjustedMax+2,
              // beginAtZero: true, // Ensure y-axis starts from 0
              ticks: {
                stepSize: 2,
                precision: 0
              },
            },
          },
        },
      });
    },


    renderRatingsChart(labels, values) {
    const ctx = document.getElementById('ratingsDoughnutChart').getContext('2d');
    if (this.ratingsChartInstance) this.ratingsChartInstance.destroy();

    this.ratingsChartInstance = new Chart(ctx, {
      type: 'doughnut',
      data: {
        // labels: labels.map(label => `${label} Stars`),
        labels:labels,
        datasets: [{
          data: values,
          backgroundColor: ['#4CAF50', '#FFEB3B', '#2196F3', '#9966FF', '#F44336', '#FF6384'],
        }],
      },
      options: {
        responsive: true,

        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Overall Ratings for the Service Requests' },
          tooltip: {
            callbacks: {
              label: (context) => {
                const label = context.label || '';
                const value = context.raw || 0;
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const percentage = ((value / total) * 100).toFixed(2);
                return `${label}: ${value} (${percentage}%)`;
              },
            },
          },
        }
      },
    });
  },

  // async generateCSVReport(){
  //     const res = await fetch("http://127.0.0.1:5000/generate_csv_report",{
  //         method:"GET",
  //         headers: {
  //           'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
  //         },
  //     })
  //     const task_id = (await res.json()).task_id
  //     const interval = setInterval(async()=>{
  //       const res = await fetch(`http://127.0.0.1:5000/download_report/${task_id}`)
  //       if(res.ok){
  //         console.log('CSV report generated successfully');
  //         alert("CSV report generated successfully")
  //         window.location.href = `http://127.0.0.1:5000/download_report/${task_id}`
  //         clearInterval(interval)
  //       }
  //     }, 100)
  // }
  async generateCSVReport() {
    const res = await fetch("http://127.0.0.1:5000/generate_csv_report", {
        method: "GET",
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
    });

    const task_id = (await res.json()).task_id;

    let isDownloaded = false; // Flag to ensure the download happens only once

    const interval = setInterval(async () => {
        if (isDownloaded) return; // Skip if the download is already triggered

        const res = await fetch(`http://127.0.0.1:5000/download_report/${task_id}`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
        });

        if (res.ok) {
            isDownloaded = true; // Set the flag to prevent further downloads
            console.log('CSV report generated successfully');
            alert("CSV report generated successfully");

            // Fetch the file as a Blob for download
            const contentDisposition = res.headers.get('Content-Disposition');
            console.log(contentDisposition);
            const filename = contentDisposition
                ? contentDisposition.split('filename=')[1].replace(/"/g, '')
                : 'report.csv';
            const blob = await res.blob();

            // Create a temporary download link
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = filename;

            // Trigger the download
            link.click();

            // Clear the interval to stop further checks
            clearInterval(interval);
        }
    }, 1000); // Checking every 1 second
}

},

};
</script>

<style scoped>
canvas {
  width: 80%;
  height: 80%;
  margin: auto;
}

</style>
