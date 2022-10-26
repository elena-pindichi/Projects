clc, clear, close all

m = 0.2; % masa bilei
g = 9.8; % acceleratia gravitationala

Ts = 0.05; % perioada

Cx = 5/7;
Cy = 5/7;

Q = [1000 0; ...
      0 1]; % R si Q sunt matrice de weight
R = 10;

N = 5; % orizontul de predictie
%% Pentru X
Adx = [1   Ts;...
       0   1];

Bdx = [0;  Cx * Ts];

%% Pentru Y
Ady = [1   Ts;...
       0   1];

Bdy = [0;  Cy * Ts];

%% Constrangeri si stari
 % Constrangerea de tip box pentru intrare u
 u_lb = -0.5;
 u_ub = 0.5;

 % Starea initiala a sistemului
 z0x = [0.06; -0.1];

 z0y = [0.06; -0.06];

 % Referintele pe care le urmarim
 phi_ref = 0;
 theta_ref = 0;
 z_ref = [0; 0];

 step = 0;
 zx = z0x;
 zy = z0y;

 u_phi = [];
 u_theta = [];

 zfx = z0x;
 zfy = z0y;
 phi = -0.1 * ones(N, 1);

%%  Aducerea bilei in centrul mesei
%  while step < 1000 
%    [Hx,qx,Cx,dx]= denseMPC(Adx, Bdx, Q, R, zx, N, u_ub, u_lb, z_ref, phi_ref);
%    [Hy,qy,Cy,dy]= denseMPC(Ady, Bdy, Q, R, zy, N, u_ub, u_lb, z_ref, theta_ref);
% %    phi = quadprog(Hx, qx, Cx, dx);
% %    theta = quadprog(Hy, qy, Cy, dy);
%     %% GRADIENT PROIECTAT
%     epsilon = 1e-5;
%     L = max(eig(Hx));
%     alfa = 1 / L;
%     dF = Hx * phi + qx;
%     while norm(dF) > epsilon
%         phi = phi - alfa * dF;
%         phi = min(u_ub, max(u_lb, phi));
%         dF = Hx * phi + qx;
%     end
%     %% BARIERA
%     tau = 1;
%     sigma = 0.6;
%     stepb = 1;
%     theta = zeros(N, 1);
%     d1 = u_ub * ones(N,1);
%     d2 = u_lb * ones(N,1);
% 
%     dF = @(x, tau) Hy * x + qy - tau * (-1 ./ (-x + d1) + (1./(x + d2)));  
%     ddF = @(x,tau) Hy - tau * (diag(-1 ./ ((-x + d1) .^ 2)) + diag(-1 ./ ((x + d2) .^ 2)));
%     while tau >= epsilon
%          while norm(dF(theta, tau)) >= epsilon && stepb <= 1e3
%             theta = theta - inv(ddF(theta, tau)) * dF(theta, tau);
%             stepb = stepb + 1;
%             if stepb == 1e3
%                 disp('S-au atins numarul maxim de iteratii.');
%                 break;
%             end
%          end
%          tau = sigma * tau;
%     end
%    u_phi = [u_phi, phi(1,1)];
%    u_theta = [u_theta, theta(1,1)];
%    znoux = Adx * zx + Bdx * phi(1,1);
%    znouy = Ady * zy + Bdy * theta(1,1);
%    zx = znoux;
%    zy = znouy;
%    zfx = [zfx zx];
%    zfy = [zfy zy];
%    step = step + 1;
%  end

%% Traiectorie patrat
 while step < 1000
   tr = puncte_patrat([zx(1), zy(1)], N);


   z_refx = [tr(1, 1); 0];
   z_refy = [tr(1, 2); 0];    
   [Hx,qx,Cx,dx]= denseMPC(Adx, Bdx, Q, R, zx, N, u_ub, u_lb, z_refx, phi_ref);
   [Hy,qy,Cy,dy]= denseMPC(Ady, Bdy, Q, R, zy, N, u_ub, u_lb, z_refy, theta_ref);

    phi = quadprog(Hx, qx, Cx, dx);
%    theta = quadprog(Hy, qy, Cy, dy);

   %% CVX
%    cvx_begin quiet
%    variable theta(N)
%    minimize(1/2 * theta' * Hy * theta + qy' * theta);
%    subject to
%    Cy * theta <= dy;
%    cvx_end

%% NEWTON PROIECTAT
    theta = zeros(N, 1);
    ddfinv = inv(Hy);
    df = Hy * theta + qy;
    stepn = 1;
    while norm(df) >= 1e-5 && stepn <= 1e4
         theta = theta - ddfinv * (Hy * theta + qy);
         theta = min(u_ub, max(u_lb, theta));
         df = Hy * theta + qy;
         stepn = stepn + 1;
         if stepn == 1e4
                disp('S-au atins numarul maxim de iteratii.');
                break;
         end
   end
   u_phi = [u_phi, phi(1,1)];
   u_theta = [u_theta, theta(1,1)];
   znoux = Adx * zx + Bdx * phi(1,1);
   znouy = Ady * zy + Bdy * theta(1,1);
   zx = znoux;
   zy = znouy;
   zfx = [zfx zx];
   zfy = [zfy zy];
   step = step + 1;
 end

%% Traiectorie circulara
%  while step < 1000
%    alfa = atan(zy(1) / zx(1));
%    if zx(1) < 0
%        alfa = alfa + pi;
%    end
% 
%    z_refx = [0.06 * cos(alfa + 0.1); 0];
%    z_refy = [0.06 * sin(alfa + 0.1); 0];
%    
%    [Hx,qx,Cx,dx]= denseMPC(Adx, Bdx, Q, R, zx, N, u_ub, u_lb, z_refx, phi_ref);
%    [Hy,qy,Cy,dy]= denseMPC(Ady, Bdy, Q, R, zy, N, u_ub, u_lb, z_refy, theta_ref);
% %    phi = quadprog(Hx, qx, Cx, dx);
% %    theta = quadprog(Hy, qy, Cy, dy);
% 
%    %% GRADIENT PROIECTAT
%     epsilon = 1e-8;
%     phi = zeros(N, 1);
%     L = max(eig(Hx));
%     alfa = 1 / L;
%     dF = Hx * phi + qx;
%     while norm(dF) > epsilon
%         phi = phi - alfa * dF;
%         phi = min(u_ub, max(u_lb, phi));
%         dF = Hx * phi + qx;
%     end
% 
%     %% BARIERA
%     tau = 1;
%     sigma = 0.6;
%     stepb = 1;
%     maxIter = 1e3;
%     epsilon = 1e-8;
%     theta = zeros(N, 1); 
%     d1 = u_ub * ones(N,1);
%     d2 = u_lb * ones(N,1);
% 
%     dF = @(x, tau) Hy * x + qy - tau * (-1 ./ (-x + d1) + (1./(x + d2)));  
%     ddF = @(x,tau) Hy - tau * (diag(-1 ./ ((-x + d1) .^ 2)) + diag(-1 ./ ((x + d2) .^ 2)));
%     
%     while tau >= epsilon
%          while norm(dF(theta, tau)) >= epsilon && stepb <= maxIter
%             theta = theta - inv(ddF(theta, tau)) * dF(theta, tau);
%             stepb = stepb + 1;
%             if stepb == maxIter
%                 disp('S-au atins numarul maxim de iteratii.');
%                 break;
%             end
%          end
%          tau = sigma * tau;
% 
%     end
% 
%    u_phi = [u_phi, phi(1,1)];
%    u_theta = [u_theta, theta(1,1)];
%    znoux = Adx * zx + Bdx * phi(1,1);
%    znouy = Ady * zy + Bdy * theta(1,1);
%    zx = znoux;
%    zy = znouy;
%    zfx = [zfx zx];
%    zfy = [zfy zy];
%    step = step + 1;
%  end


%% Plotare traiectorii si comenzi
figure('Name','Pozitia pe x')
plot(1:step+1, zfx(1,:));
figure('Name','Comanda phi')
plot(1:step, u_phi);
figure('Name','Planul xOy')
plot(zfx(1,:), zfy(1,:));
