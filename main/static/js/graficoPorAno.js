$(function () {
    var $despesaChart = $("#grafico_despesas_por_ano");
      $.ajax({
        url: $despesaChart.data("url"),
        success: function (data) {

          var ctx = $despesaChart[0].getContext("2d");

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Total de Despesas por Ano',
                backgroundColor: 'green',
                
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
                text: 'Despesas por Ano'
            }
        }
      });

    }
  });

});