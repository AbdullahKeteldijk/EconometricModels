function  [llik] = llik_fun_AR2(x,theta)

alpha=theta(1);
beta=theta(2);
sig=theta(3);
beta2 = theta(4);

u=x(3:end) - alpha - beta*x(2:end-1) - beta2*x(1:end-2);

l = -(1/2)*log(2*pi*sig) - (1/2)*u.^2/sig;

llik =mean(l);