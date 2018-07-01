function [mim, fid] = readMimImage(imgFilename)
% function mim = readMimImage(imgFilename)
%      
% Reads a MIM format image based on file name.

if (nargin ~= 1)
    help readMimImage;
    error('Require one argument: file name');
    return;
end

fid = fopen(imgFilename, 'r');
if(fid==-1)
    mim=[];
else
    fseek(fid, 0, 'eof');
    file_size = ftell(fid);
    fseek(fid,0,'bof');
    width = fread(fid, 1, 'ushort');
    height = fread(fid, 1, 'ushort');
    if( file_size > width*height && file_size < 2*width*height)
        mimImg = fread(fid, [height, width], 'uchar');
    else
        mimImg = fread(fid, [height, width], 'ushort');       
    end
    mim = mimImg';
    fclose(fid);
end
return;
