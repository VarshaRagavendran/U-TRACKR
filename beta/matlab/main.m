%% ENG 4000% SPACE RESECTION, 2D-3D POSITIONING
% main function

clc;
clear all;
close all;

%[X,Y,Z,O,P,K] = ImgResect(0,88,90,0,degtorad(45),degtorad(45))
%[X,Y,Z,O,P,K] = ImgResect(1020,1040,640,0,0,degtorad(100));

% function [XT,YT,ZT] = ImgIntersect(XA,XB,YA,YB,ZA,ZB,omegaA,omegaB,phiA,phiB,kappaA,kappaB)
[XT,YT,ZT] = ImgIntersect(9577.252,9803.241,10214.285,10219.622,555.192,555.601,1.4022,-0.1557,-0.3112,-1.7063,0.6470,0.5513);
