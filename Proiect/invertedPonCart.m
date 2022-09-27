clc, clear all, close all
%% Descrierea sistemului pendulul inversat pe un carucior
M = .5;   %Masa cartului
m = 0.2;  %Masa pendulului
b = 0.1;  %coef de fracere pt carucior
I = 0.006;%momentuk de inertie
g = 9.8;  %acceleratia gravitationala
l = 0.3;  %lungimea lantului
p = I*(M+m)+M*m*l^2; %denominator for the A and B matrices
A = [0      1              0           0;...
     0 -(I+m*l^2)*b/p  (m^2*g*l^2)/p   0;...
     0      0              0           1;...
     0 -(m*l*b)/p       m*g*l*(M+m)/p  0];
B = [     0;
     (I+m*l^2)/p;
          0;
        m*l/p];
    
Q = [10 0 0 0; ...
     0 1 0 0;...
     0 0 10 0;...
     0 0 0 1];
R = 1;
N = 3; % orizontul de predictie
% Constrangerea de tip box pentru intrare u
ub = 3; 
lb = -3;
% Starea initiala a sistemului
z0 = [2; 1 ; 0.3; 0];
% Referinta de urmarit
x_ref = 0; % nu impunem nici o referinta de urmarit pe intrare
z_ref = [0; 0; 0; 0];  % iteresati sa aducem pendulul in pozitie verticala
maxIter = 20; steps = 0;
u =[]; z=z0;
x_0 = zeros(N,1); % warm start pentru metoda bariera
%%
x = -3 * ones(3, 1);
while steps < maxIter  
   [H,q,C,d]= denseMPC(A,B,Q,R,z0,N,ub,lb, z_ref, x_ref);
   %% Quadprog
    %x = quadprog(H,q,C,d);    
    
    %% Gradient proiectat
    epsilon = 1e-5;
    L = max(eig(H));
    alfa = 1 / L;
    dF = H * x + q;
    u
    while norm(dF) > epsilon
        x = x - alfa * dF;
        x = min(ub, max(lb, x));
        dF = H * x + q;
    end

% %% CVX
%     cvx_begin
%     variable x(N)
%     minimize(1/2 * x' * H * x + q' * x);
%     subject to
%     C * x <= d;
%     cvx_end
   %% 
   u = [u,x(1,1)];
   z_new = A* z0 + B *x(1,1); 
   z0 = z_new;
   z = [z z0];
   steps = steps +1;
 end
%% --------------------------------------------
figure(1)
subplot(2,2,1)
plot(z(1,:))
legend('x Pozitia caruciorului');
hold on
subplot(2,2,2)
plot(z(2,:))
legend('Viteza caruciorului');
hold on
subplot(2,2,3)
plot(z(3,:))
legend('\phi Abaterea poziției pedulului de la echilibru');
hold on
subplot(2,2,4)
plot(z(4,:))
legend('Viteza abaterei unghiulare a pendulului');
figure(2)
plot(u);
legend('u = Forta aplicata caruciorului');



