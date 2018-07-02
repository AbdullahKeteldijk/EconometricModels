
%% ADVANCED ECONOMETRICS
%
%  MAXIMUM LIKELIHOOD ESTIMATE OF PARAMETERS OF GAUSSIAN AR(2)
%
%  Description: 
%  This code snippet shows how to optimize the log likelihood
%  and estimate the parameters  of a GAUSSIAN AR(2) model 
%  by maximum likelihood.
%
%  Francisco Blasques 2016


%% 0. Clean Workspace and Command Window

clear all   %clear workspace
clc         %clear command window     

      load AE2017_assign_p1
      total = size(data);
      N = total(2);
      T = 50;
      Errors = zeros(T,N);
      MSE_mat = zeros(N,2);
      param_mat = zeros(N,4);
      llik_mat = zeros(N,1);
for i =1:N        
%% 2. Optimization Options

      options = optimset('Display','iter',... %display iterations
                         'TolFun',1e-9,... % function value convergence criteria 
                         'TolX',1e-9,... % argument convergence criteria
                         'MaxIter',500); % maximum number of iterations    

%% 4. Initial Parameter Values
      
      x = data(:,i);  % first column of dataset
      alpha_ini = 0;  % initial value for intercept
      beta_ini = 0;   % initial value for ar coefficient
      sig_ini = 1;    % initial value for innovation variance
      beta2_ini = 0;
      
      theta_ini = [alpha_ini,beta_ini,sig_ini,beta2_ini];
      
      
%% 5. Parameter Space Bounds
        
      lb=[-1000,-1000,0.00001,-1000];  % lower bound for theta
      ub=[1000,1000,1000,1000];        % upper bound for theta
      
      
%% 6. Optimize Log Likelihood Criterion
      
      % fmincon input:
      % (1) negative log likelihood function: - llik_fun_AR1()
      % (2) initial parameter: theta_ini
      % (3) parameter space bounds: lb & ub
      % (4) optimization setup: options
      %  Note: a number of parameter restriction are left empty with []

      % fmincon output:
      % (1) parameter estimates: theta_hat
      % (2) log likelihood function value at theta_hat: ls_val
      % (3) exit flag indicating (no) convergence: exitflag
      
      [theta_hat,llik_val,exitflag]=...
          fmincon(@(theta) - llik_fun_AR2(x,theta),theta_ini,[],[],[],[],lb,ub,[],options);
      
 
%% 7. Forecast 

alpha=theta_hat(1);
beta=theta_hat(2);
beta2=theta_hat(4);
sigma=theta_hat(3);



epsilon = sigma*randn(T,1);
xf = zeros(T,1);
xf(1) = x(end);
xf(2) = x(end-1);
xr = data(456:end,1);
    for t=3:T % start recursion from t=2 to t=T
        
       xf(t) =  alpha + beta * xf(t-1) + beta2 * xf(t-2) + epsilon(t); % generate x(t) recursively
       u = x(3:end) - alpha - beta*x(2:end-1) - beta2*x(1:end-2);
       %u = xf(2:end) - alpha - beta*xf(1:end-1);
    end % end recursion

    
MSE = mean((xf-xr).^2)
RMSE = sqrt(MSE)
MSE_mat(i,1) = MSE;
MSE_mat(i,2) = RMSE;
f_error = xf-xr;
Errors(:,i) = f_error;

param_mat(i,1) = alpha;
param_mat(i,2) = beta;
param_mat(i,3) = beta2;
param_mat(i,4) = sigma;

llik_mat(i) = llik_val;
end

DM_Scores = zeros(N,N);
for i=1:N
   for j=1:N 
        DM_Scores(i,j) = DM(Errors(:,i),Errors(:,j),1);
   end
end
DM_Scores
MSE_mat
param_mat
llik_mat
%% 8. Print Output


%figure1 = figure(1);
%set(figure1)
%subplot(2,1,1)
%plot(xf,'b')
%title('Forecasted')
%subplot(2,1,2)
%plot(xr,'r')
%title('Realized')      


%display('parameter estimates:')
%theta_hat

%display('log likelihood value:')
%llik_val

%display('exit flag:')
%exitflag




