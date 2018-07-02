function  [llik] = llik_fun_AR2(x,theta)

alpha=theta(1);
beta=theta(2);
sig=theta(3);
beta2 = theta(4);
beta3 = theta(5);

u=x(4:end) - alpha - beta*x(3:end-1) - beta2*x(2:end-2) - beta3*x(1:end-3);

l = -(1/2)*log(2*pi*sig) - (1/2)*u.^2/sig;

llik =mean(l);