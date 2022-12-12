$(function () {
    var $categoriaChart = $("#grafico_por_categoria");
      $.ajax({
        url: $categoriaChart.data("url"),
        success: function (data) {

          var ctx = $categoriaChart[0].getContext("2d");

          new Chart(ctx, {
            type: 'bar',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Despesas por categoria',
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
                text: 'Despesas por categoria'
            }
        }
      });

    }
  });

});