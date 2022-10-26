function [traiectorie] = puncte_patrat(z0, N)

pct = -linspace(-0.06, 0.06, 5);
X = zeros(16, 2);
X(1:5, 1) = 0.06;
X(1:5, 2) = pct;

X(6:9, 1) = pct(2:5);
X(6:9, 2) = -0.06;

X(10:13, 1) = -0.06;
X(10:13, 2) = -pct(2:5);

X(14:16, 1) = -pct(2:4);
X(14:16, 2) = 0.06;

Patrat = X;

dif = z0 - Patrat;
for i = 1 : 16
    new_dif(i) = norm(dif(i, :));
end

[~, poz] = min(new_dif);

if poz + N + 1<= 16
    traiectorie = Patrat(poz + 1:poz+N, :);
else
    traiectorie = [Patrat(poz + 1:16, :); Patrat(1 : poz + N - 16, :)];
end

% if poz ==    16
%     traiectorie = Patrat(1, :);
% else
%     traiectorie = Patrat(poz + 1, :);
% end


end

