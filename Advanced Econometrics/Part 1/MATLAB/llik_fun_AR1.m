function  [llik] = llik_fun_AR1(x,theta)

alpha=theta(1);
beta=theta(2);
sig=theta(3);


u=x(2:end) - alpha - beta*x(1:end-1); 

l = -(1/2)*log(2*pi*sig) - (1/2)*u.^2/sig;

llik =mean(l);