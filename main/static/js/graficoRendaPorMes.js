$(function () {
    var $despesaChart = $("#grafico_renda_por_mes");
      $.ajax({
        url: $despesaChart.data("url"),
        success: function (data) {

          var ctx = $despesaChart[0].getContext("2d");

          new Chart(ctx, {
            type: 'doughnut',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Total de Renda por Mês',
                backgroundColor:[
                    '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
                ],
                
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
                text: 'Receita por Mês'
            }
        }
      });

    }
  });

});