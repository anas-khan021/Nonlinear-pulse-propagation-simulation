% SiNxccub2.m
%
% Model exported on Sep 14 2016, 11:35 by COMSOL 5.1.0.145.
% Modified 2017-05-09

clear variables, close all

import com.comsol.model.*
import com.comsol.model.util.*

model = ModelUtil.create('Model');

model.modelPath('/user1/icb/au4287co/matlab/DispersionGuide/SiNx');

model.label('SiNx-ccub.mph');

model.comments(['sans titre\n\n']);

model.param.set('Gwidth', '1', 'Guide''s width');
model.param.set('Gheight', '0.4', 'Guide''s height');
model.param.set('Bwidth', '10', 'Box width');
model.param.set('SellCA', '0.1730');
model.param.set('SellCB', '0.2294');
model.param.set('SellCC', '3.9887');
model.param.set('SellCD', '0.0457');
model.param.set('clight', '3e8', 'Light speed');
model.param.set('wavelength', '1.55e-6');
model.param.set('Sheight', '0.69');

model.modelNode.create('comp1');

model.file.clear;

model.func.create('an2', 'Analytic');
model.func.create('an3', 'Analytic');
model.func('an2').label('nSil');
model.func('an2').set('expr', 'sqrt(1+0.6961663*x^2/(x^2-0.0684043^2)+0.4079426*x^2/(x^2-0.1162414^2)+0.8974794*x^2/(x^2-9.896161^2))');
model.func('an2').set('plotargs', {'x' '0.6' '4'});
model.func('an2').set('funcname', 'nSil');
model.func('an3').label('nSiNxPoly');
model.func('an3').set('expr', 'sqrt(-0.018793231081268*x^7+0.247357662902859*x^6-1.364117938855824*x^5+4.140065514321793*x^4-7.559941650373040*x^3+8.409802179403169*x^2-5.442240807372252*x+4.951827631830032+1)');
model.func('an3').set('plotargs', {'x' '0.6' '4'});
model.func('an3').set('funcname', 'nSiNxPoly');

model.func.create('int1', 'Interpolation');
model.func('int1').label('nSiNxInt');
model.func('int1').set('extrap', 'interior');
model.func('int1').set('interp', 'piecewisecubic');
model.func('int1').set('filename', '/user1/icb/au4287co/matlab/DispersionGuide/SiNx/SiNx_FilterMoy1.txt');
model.func('int1').set('source', 'file');
model.func('int1').set('funcs', {'nSiNxInt' '1'});

model.geom.create('geom1', 2);

model.mesh.create('mesh1', 'geom1');

model.geom('geom1').lengthUnit([native2unicode(hex2dec({'00' 'b5'}), 'unicode') 'm']);
model.geom('geom1').create('r1', 'Rectangle');
model.geom('geom1').feature('r1').label('Superstrate');
model.geom('geom1').feature('r1').setIndex('layer', '0.5', 0);
model.geom('geom1').feature('r1').set('layerbottom', false);
model.geom('geom1').feature('r1').set('size', {'Bwidth' 'Bwidth/2'});
model.geom('geom1').feature('r1').set('layertop', true);
model.geom('geom1').feature('r1').set('layerleft', true);
model.geom('geom1').feature('r1').set('pos', {'0' 'Bwidth/4'});
model.geom('geom1').feature('r1').set('base', 'center');
model.geom('geom1').feature('r1').set('layername', {'SupPML'});
model.geom('geom1').feature('r1').set('layerright', true);
model.geom('geom1').create('r2', 'Rectangle');
model.geom('geom1').feature('r2').label('Substrate');
model.geom('geom1').feature('r2').setIndex('layer', '0.5', 0);
model.geom('geom1').feature('r2').set('size', {'Bwidth' 'Bwidth/2'});
model.geom('geom1').feature('r2').set('layerleft', true);
model.geom('geom1').feature('r2').set('pos', {'0' '-Bwidth/4'});
model.geom('geom1').feature('r2').set('base', 'center');
model.geom('geom1').feature('r2').set('layername', {'SubPML'});
model.geom('geom1').feature('r2').set('layerright', true);
model.geom('geom1').create('r4', 'Rectangle');
model.geom('geom1').feature('r4').label('Strate');
model.geom('geom1').feature('r4').set('size', {'Bwidth' 'Sheight-Gheight'});
model.geom('geom1').feature('r4').set('pos', {'0' '(Sheight-Gheight)/2'});
model.geom('geom1').feature('r4').set('base', 'center');
model.geom('geom1').create('r3', 'Rectangle');
model.geom('geom1').feature('r3').label('Guide');
model.geom('geom1').feature('r3').set('size', {'Gwidth' 'Gheight'});
model.geom('geom1').feature('r3').set('pos', {'0' 'Sheight-Gheight+Gheight/2'});
model.geom('geom1').feature('r3').set('base', 'center');
model.geom('geom1').run;
model.geom('geom1').run('fin');

model.material.create('mat2', 'Common', 'comp1');
model.material.create('mat3', 'Common', 'comp1');
model.material.create('mat4', 'Common', 'comp1');
model.material('mat2').selection.set([1 2 6 7 12 13]);
model.material('mat2').propertyGroup.create('RefractiveIndex', ['Indice de r' native2unicode(hex2dec({'00' 'e9'}), 'unicode') 'fraction']);
model.material('mat3').selection.set([4 5 9 10 15 16]);
model.material('mat3').propertyGroup.create('RefractiveIndex', ['Indice de r' native2unicode(hex2dec({'00' 'e9'}), 'unicode') 'fraction']);
model.material('mat4').selection.set([3 8 11 14]);
model.material('mat4').propertyGroup.create('RefractiveIndex', ['Indice de r' native2unicode(hex2dec({'00' 'e9'}), 'unicode') 'fraction']);

model.coordSystem.create('pml1', 'geom1', 'PML');

model.physics.create('emw', 'ElectromagneticWaves', 'geom1');

model.mesh('mesh1').create('size1', 'Size');
model.mesh('mesh1').create('size2', 'Size');
model.mesh('mesh1').create('ftri1', 'FreeTri');
model.mesh('mesh1').feature('size1').selection.geom('geom1', 2);
model.mesh('mesh1').feature('size1').selection.set([3 8 11 14]);
model.mesh('mesh1').feature('size2').selection.geom('geom1', 2);
model.mesh('mesh1').feature('size2').selection.set([1 2 6 7 12 13]);

% model.view('view1').axis.set('abstractviewxscale', '0.02107279747724533');
% model.view('view1').axis.set('ymin', '-5.5');
% model.view('view1').axis.set('xmax', '6.94348669052124');
% model.view('view1').axis.set('abstractviewyscale', '0.02107279747724533');
% model.view('view1').axis.set('abstractviewbratio', '-0.05000000074505806');
% model.view('view1').axis.set('abstractviewtratio', '0.05000000074505806');
% model.view('view1').axis.set('abstractviewrratio', '0.19434866309165955');
% model.view('view1').axis.set('xmin', '-6.94348669052124');
% model.view('view1').axis.set('abstractviewlratio', '-0.19434866309165955');
% model.view('view1').axis.set('ymax', '5.5');

model.material('mat2').label('Substrate');
model.material('mat2').propertyGroup('RefractiveIndex').set('n', '');
model.material('mat2').propertyGroup('RefractiveIndex').set('ki', '');
model.material('mat2').propertyGroup('RefractiveIndex').set('n', {'nSil(wavelength*1e6)' '0' '0' '0' 'nSil(wavelength*1e6)' '0' '0' '0' 'nSil(wavelength*1e6)'});
model.material('mat2').propertyGroup('RefractiveIndex').set('ki', {'0' '0' '0' '0' '0' '0' '0' '0' '0'});
model.material('mat3').label('Superstrate');
model.material('mat3').propertyGroup('RefractiveIndex').set('n', '');
model.material('mat3').propertyGroup('RefractiveIndex').set('ki', '');
model.material('mat3').propertyGroup('RefractiveIndex').set('n', {'1' '0' '0' '0' '1' '0' '0' '0' '1'});
model.material('mat3').propertyGroup('RefractiveIndex').set('ki', {'0' '0' '0' '0' '0' '0' '0' '0' '0'});
model.material('mat4').label('SiNx');
model.material('mat4').propertyGroup('RefractiveIndex').set('n', '');
model.material('mat4').propertyGroup('RefractiveIndex').set('ki', '');
model.material('mat4').propertyGroup('RefractiveIndex').set('n', {'nSiNxPoly(wavelength*1e6)' '0' '0' '0' 'nSiNxPoly(wavelength*1e6)' '0' '0' '0' 'nSiNxPoly(wavelength*1e6)'});
% model.material('mat4').propertyGroup('RefractiveIndex').set('n', {'nSiNxInt(wavelength*1e6)' '0' '0' '0' 'nSiNxInt(wavelength*1e6)' '0' '0' '0' 'nSiNxInt(wavelength*1e6)'});
% model.material('mat4').propertyGroup('RefractiveIndex').set('n', {'2.07' '0' '0' '0' '2.07' '0' '0' '0' '2.07'});
model.material('mat4').propertyGroup('RefractiveIndex').set('ki', {'0' '0' '0' '0' '0' '0' '0' '0' '0'});

model.physics('emw').feature('wee1').set('DisplacementFieldModel', 'RefractiveIndex');

model.mesh('mesh1').feature('size').set('custom', 'on');
model.mesh('mesh1').feature('size').set('hnarrow', '3');
model.mesh('mesh1').feature('size').set('hgrad', '1.2');
model.mesh('mesh1').feature('size').set('hcurve', '0.1');
model.mesh('mesh1').feature('size').set('hmax', '1');
model.mesh('mesh1').feature('size1').set('hauto', 1);
model.mesh('mesh1').feature('size1').set('custom', 'on');
model.mesh('mesh1').feature('size1').set('hnarrowactive', true);
model.mesh('mesh1').feature('size1').set('hnarrow', '5');
model.mesh('mesh1').feature('size1').set('hmaxactive', true);
model.mesh('mesh1').feature('size1').set('hmax', '0.06');
model.mesh('mesh1').feature('size2').set('hauto', 3);
model.mesh('mesh1').feature('size2').set('custom', 'on');
model.mesh('mesh1').feature('size2').set('hgradactive', true);
model.mesh('mesh1').feature('size2').set('hnarrowactive', true);
model.mesh('mesh1').feature('size2').set('hnarrow', '3');
model.mesh('mesh1').feature('size2').set('hmaxactive', true);
model.mesh('mesh1').feature('size2').set('hgrad', '1.2');
model.mesh('mesh1').feature('size2').set('hmax', '1');
model.mesh('mesh1').run;

model.study.create('std1');
model.study('std1').create('mode', 'ModeAnalysis');

model.sol.create('sol1');
model.sol('sol1').study('std1');
model.sol('sol1').attach('std1');
model.sol('sol1').create('st1', 'StudyStep');
model.sol('sol1').create('v1', 'Variables');
model.sol('sol1').create('e1', 'Eigenvalue');

model.study('std1').feature('mode').set('initstudyhide', 'on');
model.study('std1').feature('mode').set('initsolhide', 'on');
model.study('std1').feature('mode').set('solnumhide', 'on');
model.study('std1').feature('mode').set('notstudyhide', 'on');
model.study('std1').feature('mode').set('notsolhide', 'on');
model.study('std1').feature('mode').set('notsolnumhide', 'on');

% model.result.dataset.create('an3_ds1', 'Grid1D');
% model.result.dataset.create('an3_ds2', 'Grid1D');
% model.result.dataset.create('an3_ds3', 'Grid1D');
% model.result.dataset.create('an3_ds4', 'Grid1D');
% model.result.dataset('an3_ds1').set('data', 'none');
% model.result.dataset('an3_ds2').set('data', 'none');
% model.result.dataset('an3_ds3').set('data', 'none');
% model.result.dataset('an3_ds4').set('data', 'none');
% model.result.create('pg1', 'PlotGroup2D');
% model.result('pg1').create('surf1', 'Surface');

model.study('std1').feature('mode').set('modeFreq', 'clight/wavelength');
model.study('std1').feature('mode').set('neigs', '4');
model.study('std1').feature('mode').set('shift', '2');

model.sol('sol1').attach('std1');
model.sol('sol1').feature('e1').set('neigs', '4');
model.sol('sol1').feature('e1').set('transform', 'effective_mode_index');
model.sol('sol1').feature('e1').set('shift', '2');
model.sol('sol1').feature('e1').feature('aDef').set('complexfun', true);
% model.sol('sol1').runAll;

% model.result.dataset('an3_ds1').set('parmin1', '0.6');
% model.result.dataset('an3_ds1').set('function', 'an3');
% model.result.dataset('an3_ds1').set('parmax1', '4');
% model.result.dataset('an3_ds2').set('parmin1', '0.6');
% model.result.dataset('an3_ds2').set('function', 'an3');
% model.result.dataset('an3_ds2').set('parmax1', '4');
% model.result.dataset('an3_ds3').set('parmin1', '0.6');
% model.result.dataset('an3_ds3').set('function', 'all');
% model.result.dataset('an3_ds3').set('parmax1', '4');
% model.result.dataset('an3_ds4').set('parmin1', '0.6');
% model.result.dataset('an3_ds4').set('function', 'all');
% model.result.dataset('an3_ds4').set('parmax1', '4');
% model.result('pg1').label(['Champ ' native2unicode(hex2dec({'00' 'e9'}), 'unicode') 'lectrique (emw)']);
% model.result('pg1').set('looplevel', {'4'});
% model.result('pg1').set('frametype', 'spatial');

Sheight = str2num(model.param.get('Sheight'));

% Gwidth = 2.6:0.2:3.6;
for Gwidth = 3.5:0.2:3.5;
    Gwidth
    model.param.set('Gwidth', num2str(Gwidth), 'Guide''s width');

    neff = [];
    absorption = [];
    wavelengthTab = 1.0e-6:0.02e-6:3.0e-6;
%     wavelengthTab = 1.5e-6:0.02e-6:1.5e-6;
%     p = [-0.018793231081268 0.247357662902859 -1.364117938855824 4.140065514321793 -7.559941650373040 8.409802179403169 -5.442240807372252   4.951827631830032];

    for wavelength = wavelengthTab;
        wavelength
        model.param.set('wavelength', num2str(wavelength));
        model.study('std1').feature('mode').set('modeFreq', 'clight/wavelength');
    %     nSiNx_temp = sqrt(polyval(p, wavelength*1e6) + 1);
    %     model.material('mat4').propertyGroup('RefractiveIndex').set('n', {num2str(nSiNx_temp,16) '0' '0' '0' num2str(nSiNx_temp,16) '0' '0' '0' num2str(nSiNx_temp,16)});

        model.sol('sol1').runAll;
        neff_temp = mphglobal(model, {'emw.neff'})
        abs_temp = mphglobal(model, {'emw.neff*i'});
        ExCenter = mphinterp(model, {'abs(emw.Ex)'}, 'coord', [0;Sheight/2]); % Get Ex field in the center
%         ExMax = mphmax(model, {'abs(emw.Ex)'}, 2); % Get max of Ex field
        ExInt = mphint2(model, {'abs(emw.Ex)'}, 2); % Get integral of Ex field on the whole simulation area
        
%         % Get field profile in the center of the waveguide
%         x0 = linspace(-Gwidth/2-1,Gwidth/2+1,100);
%         y0 = Sheight/2; % Center of the waveguide
%         [x, y] = meshgrid(x0, y0);
%         xx = [x(:),y(:)]';
%         % Get the values from comsol
%         Ex = mphinterp(model, 'abs(emw.Ex)', 'coord', xx);
        
        ExRatio = ExCenter./ExInt'; % Because TE mode should have max Ex in center of waveguide
        SortOutput = sortrows([ExRatio neff_temp abs_temp]);
        neff = [neff SortOutput(:,2)];
        absorption = [absorption SortOutput(:,3)];
    end

    figure('Position', [100, 100, 1000, 700]);
    subplot(2,1,1)
    plot(wavelengthTab, neff, '.')
    xlabel('Wavelength [m]'), ylabel('Indices')
    xlim([min(wavelengthTab) max(wavelengthTab)])

    c = 3e8; % m/s
    w = 2*pi*c./(wavelengthTab); % rad/s
    
    beta = neff(end,:)*2*pi./wavelengthTab; % m^-1
    beta1 = gradient(beta)./gradient(w);
    beta2 = gradient(beta1)./gradient(w);
    vg = gradient(w)./gradient(beta);
    b = gradient(1./vg)./gradient(w);
    GVD = b;
    D = -2*pi*c./(wavelengthTab.^2).*GVD;
    
    subplot(2,1,2)
    plot(wavelengthTab, GVD, '.')
    xlabel('Wavelength [m]'), ylabel('GVD [fs^2/m]')
    grid on, xlim([min(wavelengthTab) max(wavelengthTab)])
    
    dispParams = [wavelengthTab; beta; absorption(end,:)]';
    save('-ascii', strcat('dispParams-Gwidth-', num2str(Gwidth), '.dat'), 'dispParams');

    dispGVD = [wavelengthTab; GVD; D]';
    save('-ascii', strcat('dispGVD-Gwidth-', num2str(Gwidth), '.dat'), 'dispGVD');
end
