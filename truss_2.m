% The system of linear equations for the Truss Problem
A = [1/sqrt(2) 0 0 -1 -1/sqrt(2) 0 0 0 0 0 0 0 0;
     1/sqrt(2) 0 1  0  1/sqrt(2) 0 0 0 0 0 0 0 0;
     0         0 1  0  0         0 0 0 0 0 0 0 0;
     0         1 0  0  0         1 0 0 0 0 0 0 0;
     0         0 0  0  0         0 1 0 0 0 0 0 0;
     0         0 0  1  0         0 0 -1 0 0 0 0 0;
     0 0 0 0 1/sqrt(2) 0 1 0 1/sqrt(2) 0 0 0 0;
     0 0 0 0 1/sqrt(2) 1 0 0 -1/sqrt(2) -1 0 0 0;
     0 0 0 0 0 0 0 1 1/sqrt(2) 0 0 -1/sqrt(2) 0;
     0 0 0 0 0 0 0 0 1/sqrt(2) 0 1 1/sqrt(2) 0;
     0 0 0 0 0 0 0 0 0 0 1 0 0;
     0 0 0 0 0 0 0 0 0 1 0 0 -1;
     0 0 0 0 0 0 0 0 0 0 0 1/sqrt(2) 1];

% To solve Ax = b
b = [0; 0; 10; 0; 0; 0; 15; 0; 0; 0; 10; 0; 0];

% x is the solution to the linear system
x = A\b;
vals = abs((x/sum(abs(x)))*15);
disp(vals)

% Plotting the result vector
x_1 = 0:1/10:1;
y_1 = x_1;

figure % new figure window
plot(x_1, y_1, 'r','LineWidth', vals(1));
axis off;

hold on;
x_2 = 0:1/10:1;
y_2 = x_2*0;
plot(x_2, y_2, 'r', 'LineWidth', vals(2));

y_3 = 0:1/10:1;
x_3 = y_3*0 + 1;
plot(x_3, y_3, 'b', 'LineWidth',vals(3));

x_4 = 1:1/10:2;
y_4 = x_4*0 + 1;
plot(x_4, y_4, 'r','LineWidth', vals(4));

x_5 = 1:1/10:2;
y_5 = -x_5+2;
plot(x_5, y_5, 'b','LineWidth', vals(5));

x_6 = 1:1/10:2;
y_6 = x_2*0;
plot(x_6, y_6, 'b', 'LineWidth',vals(6));

y_7 = 0:1/10:1;
x_7 = y_7*0 + 2;
plot(x_7, y_7, '--');

x_8 = 2:1/10:3;
y_8 = x_8*0 + 1;
plot(x_8, y_8, 'r', 'LineWidth',vals(8));

x_9 = 2:1/10:3;
y_9 = x_9-2;
plot(x_9, y_9, 'b','LineWidth', vals(9));

x_10 = 2:1/10:3;
y_10 = x_10*0;
plot(x_10, y_10, 'b','LineWidth', vals(10));

y_11 = 0:1/10:1;
x_11 = y_11*0 + 3;
plot(x_11, y_11, 'b', 'LineWidth',vals(11));

x_12 = 3:1/10:4;
y_12 = -x_12+4;
plot(x_12, y_12, 'r', 'LineWidth',vals(12));

x_13 = 3:1/10:4;
y_13 = x_13*0;
plot(x_13, y_13, 'b','LineWidth', vals(13));
hold off;