﻿'use strict';

function BinaryWriter()
{
    this._writers = [];
    this._length = 0;
}

module.exports = BinaryWriter;

/* Pass string */
BinaryWriter.prototype.writeArray = function (str)  {
    var escstr = encodeURIComponent(str);
    var binstr = escstr.replace(/%([0-9A-F]{2})/g, function(match, p1) {
        return String.fromCharCode('0x' + p1);
    });
    var ua = new Uint8Array(binstr.length);
    Array.prototype.forEach.call(binstr, function (ch, i) {
        ua[i] = ch.charCodeAt(0);
    });
    return ua;
};

BinaryWriter.prototype.writeUInt8 = function(value)
{
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        buffer.writeUInt8(value, offset, true);
    });
    this._length += 1;
};

BinaryWriter.prototype.writeInt8 = function(value)
{
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        buffer.writeInt8(value, offset, true);
    });
    this._length += 1;
};

BinaryWriter.prototype.writeUInt16 = function(value)
{
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        buffer.writeUInt16LE(value, offset, true);
    });
    this._length += 2;
};

BinaryWriter.prototype.writeInt16 = function(value)
{
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        buffer.writeInt16LE(value, offset, true);
    });
    this._length += 2;
};

BinaryWriter.prototype.writeUInt32 = function(value)
{
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        buffer.writeUInt32LE(value, offset, true);
    });
    this._length += 4;
};

BinaryWriter.prototype.writeInt32 = function(value)
{
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        buffer.writeInt32LE(value, offset, true);
    });
    this._length += 4;
};

BinaryWriter.prototype.writeFloat = function(value)
{
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        buffer.writeFloatLE(value, offset, true);
    });
    this._length += 4;
};

BinaryWriter.prototype.writeDouble = function(value)
{
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        buffer.writeDoubleLE(value, offset, true);
    });
    this._length += 8;
};

BinaryWriter.prototype.writeBytes = function(data)
{
    var length = data.length;
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        data.copy(buffer, offset, 0, length);
    });
    this._length += length;
};

BinaryWriter.prototype.writeStringUtf8 = function(value)
{
    var length = Buffer.byteLength(value, 'utf8')
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        buffer.write(value, offset, 'utf8');
    });
    this._length += length;
};

BinaryWriter.prototype.writeStringUnicode = function(value)
{
    var length = Buffer.byteLength(value, 'ucs2')
    var offset = this._length;
    this._writers.push(function(buffer)
    {
        buffer.write(value, offset, 'ucs2');
    });
    this._length += length;
};

BinaryWriter.prototype.writeStringZeroUtf8 = function(value)
{
    this.writeStringUtf8(value);
    this.writeUInt8(0);
};

BinaryWriter.prototype.writeStringZeroUnicode = function(value)
{
    this.writeStringUnicode(value);
    this.writeUInt16(0);
};

BinaryWriter.prototype.toBuffer = function()
{
    var buffer = new Buffer(this._length);
    for (var i = 0; i < this._writers.length; i++)
    {
        this._writers[i](buffer);
    }
    return buffer;
};
