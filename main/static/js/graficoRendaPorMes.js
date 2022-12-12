$(function () {
    var $rendaChart = $("#grafico_renda_por_mes");
      $.ajax({
        url: $rendaChart.data("url"),
        success: function (data) {

          var ctx = $rendaChart[0].getContext("2d");

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Total de Renda por Mês',
                backgroundColor:'blue',
                
                data: data.data
              }]          
            },
            options: {
              responsive: true,
              legend: {
                position: 'top',
              },
              title: {
                display: true,
                text: 'Renda por Mês'
            }
        }
      });

    }
  });

});
