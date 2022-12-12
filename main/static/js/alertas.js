const usernameField=document.querySelector('#usernameField');
const userFeedBackError = document.querySelector(".user_feedback_error");
const emailField=document.querySelector('#emailField');
const emailFeedbackError = document.querySelector(".email_feedback_error");
const mostrarSenha = document.querySelector(".mostrarSenha"); 
const passwordField = document.querySelector("#passwordField");

// Pega o que o usuário está digiranto
usernameField.addEventListener("keyup", (e) => {
    const usernameValue = e.target.value;
    usernameField.classList.remove("is-invalid");
    userFeedBackError.style.display = "none";

    if(usernameValue.length > 0){
        // Chama a API
        fetch("/autenticacao/valida_usuario", {
            // Especifica o que vai ser enviado através do  post. 
            // O stringfy tranforma o objeto javascript em JSON para que possa ser enviado
            body: JSON.stringify({ username: usernameValue }), //chave(username) e valor(usernameValue)
            method: "POST",
        // O fetch retorna uma promessa, que irá retornar outra promessa, mapear o json e então retornar os dados.
        })
        .then((res) => res.json())
        .then((data) => {
        console.log("data", data)
        if (data.error_usuario){
            usernameField.classList.add("is-invalid");
            //Exibe alerta de erro no formulário
            userFeedBackError.style.display = "block";
            userFeedBackError.innerHTML = `<p>${data.error_usuario}</p>`;
        }
        });
    }
});

emailField.addEventListener("keyup", (e) => {
    const emailValue = e.target.value;
    emailField.classList.remove("is-invalid");
    emailFeedbackError.style.display = "none";
    if(emailValue.length > 0){
        fetch("/autenticacao/validacao_email", {
            body: JSON.stringify({ email: emailValue }), 
            method: "POST",
        })  
        .then((res) => res.json())
        .then((data) => {
        console.log("data", data)
        if (data.error_email){
            emailFeedbackError.style.display = "block";
            emailFeedbackError.innerHTML = `<p>${data.error_email}</p>`;
        } 
        });
    }
});

const handleInput = (e) => {
    if(mostrarSenha.textContent === 'Exibir senha'){
        mostrarSenha.textContent = "Esconder";
        passwordField.setAttribute("type", "text");
    } else {
        mostrarSenha.textContent = "Exibir senha";
        passwordField.setAttribute("type", "password");
    }
}

mostrarSenha.addEventListener('click',handleInput);