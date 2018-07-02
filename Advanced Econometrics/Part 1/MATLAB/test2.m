function  [llik] = llik_fun_test2(x,theta)

alpha=theta(1);
beta=theta(2);
sig=theta(3);
gamma = theta(4);
delta = theta(5);
mu = theta(6);
%g = zeros(T, 1);
%g(1) = 1; 
g = delta + (gamma/(1+exp(beta*(x(1:end-1)-mu).^2)));

u=x(2:end) - alpha - g*x(1:end-1); 

l = -(1/2)*log(2*pi*sig) - (1/2)*u.^2/sig;

llik =mean(l);