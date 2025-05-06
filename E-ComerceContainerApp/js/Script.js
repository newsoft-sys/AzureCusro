let cartItems = [];
let cartTotal = 0;

function addToCart(name, price) {
    cartItems.push({ name, price });
    cartTotal += price;

    // Atualizar o carrinho na página
    const cartItemsList = document.getElementById('cart-items');
    const cartTotalElement = document.getElementById('cart-total');

    const li = document.createElement('li');
    li.textContent = `${name} - R$ ${price}`;
    cartItemsList.appendChild(li);

    cartTotalElement.textContent = cartTotal;
}

function finalizeOrder() {
    // Salvar os itens do carrinho no localStorage
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    localStorage.setItem('cartTotal', cartTotal);

    // Redirecionar para a página de resumo do pedido
    window.location.href = 'order-summary.html';
}