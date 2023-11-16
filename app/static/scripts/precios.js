const segundoInput = document.getElementById('segundo');
const minutoInput = document.getElementById('minuto');
const horaInput = document.getElementById('hora');
const diaInput = document.getElementById('dia');
const precioInput = document.getElementById('txtPrecio');

    precioInput.addEventListener('input', () => {
        if (precioInput.value < 0) {
            precioInput.value = 0;
        }
        if (precioInput.value > 10000) {
            precioInput.value = 10000;
        }
    });

    segundoInput.addEventListener('input', () => {
        if (segundoInput.value >= 60) {
            segundoInput.value = 0;
            minutoInput.value++;
        }
        if(segundoInput.value < 0){
            segundoInput.value = 59;
            minutoInput.value--;
        }
        if(minutoInput.value < 0){
            minutoInput.value = 59;
            horaInput.value--;
        }
        if(horaInput.value < 0){
            horaInput.value = 23;
            diaInput.value--;
        }
        if(diaInput.value < 0){
            diaInput.value = 0;
        }
        if(minutoInput.value >= 60){
            minutoInput.value = 0;
            horaInput.value++;
        }
        if(horaInput.value >= 24){
            horaInput.value = 0;
            diaInput.value++;
        }
    });

    minutoInput.addEventListener('input', () => {
        if (minutoInput.value >= 60) {
            minutoInput.value = 0;
            horaInput.value++;
        }
        if(minutoInput.value < 0){
            minutoInput.value = 59;
            horaInput.value--;
        }
        if(horaInput.value < 0){
            horaInput.value = 23;
            diaInput.value--;
        }
        if(diaInput.value < 0){
            diaInput.value = 0;
        }
        if(horaInput.value >= 24){
            horaInput.value = 0;
            diaInput.value++;
        }

    });
    
    horaInput.addEventListener('input', () => {
        if (horaInput.value >= 24) {
            horaInput.value = 0;
            diaInput.value++;
        }
        if(horaInput.value < 0){
            horaInput.value = 23;
            diaInput.value--;
        }
        if(diaInput.value < 0){
            diaInput.value = 0;
        }
    });

    diaInput.addEventListener('input', () => {
        if(diaInput.value < 0){
            diaInput.value = 0;
        }
        if(diaInput.value > 30){
            diaInput.value = 30;
        }
    });