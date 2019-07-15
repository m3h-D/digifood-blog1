(function webpackUniversalModuleDefinition(root, factory) {
    if (typeof exports === 'object' && typeof module === 'object')
        module.exports = factory(); else if (typeof define === 'function' && define.amd)
        define("whatInput", [], factory); else if (typeof exports === 'object')
        exports.whatInput = factory(); else root.whatInput = factory()
})(this, function () {
    return (function (modules) {
        var installedModules = {}; function __webpack_require__(moduleId) {
            if (installedModules[moduleId])
                return installedModules[moduleId].exports; var module = installedModules[moduleId] = { exports: {}, id: moduleId, loaded: !1 }; modules[moduleId].call(module.exports, module, module.exports, __webpack_require__); module.loaded = !0; return module.exports;/******/
        }
        __webpack_require__.m = modules; __webpack_require__.c = installedModules; __webpack_require__.p = ""; return __webpack_require__(0);/******/
    })([(function (module, exports) {
        'use strict'; module.exports = function () {
            var currentInput = 'initial'; var currentIntent = null; var doc = document.documentElement; var formInputs = ['input', 'select', 'textarea']; var functionList = []; var ignoreMap = [16, 17, 18, 91, 93]; var changeIntentMap = [9]; var inputMap = { keydown: 'keyboard', mousedown: 'mouse', mousemove: 'mouse', MSPointerDown: 'pointer', MSPointerMove: 'pointer', pointerdown: 'pointer', pointermove: 'pointer', touchstart: 'touch' }; var inputTypes = []; var isBuffering = !1; var isScrolling = !1; var mousePos = { x: null, y: null }; var pointerMap = { 2: 'touch', 3: 'touch', 4: 'mouse' }; var supportsPassive = !1; try { var opts = Object.defineProperty({}, 'passive', { get: function get() { supportsPassive = !0 } }); window.addEventListener('test', null, opts) } catch (e) { }
            var setUp = function setUp() { inputMap[detectWheel()] = 'mouse'; addListeners(); setInput() }; var addListeners = function addListeners() {
                if (window.PointerEvent) { doc.addEventListener('pointerdown', updateInput); doc.addEventListener('pointermove', setIntent) } else if (window.MSPointerEvent) { doc.addEventListener('MSPointerDown', updateInput); doc.addEventListener('MSPointerMove', setIntent) } else { doc.addEventListener('mousedown', updateInput); doc.addEventListener('mousemove', setIntent); if ('ontouchstart' in window) { doc.addEventListener('touchstart', touchBuffer); doc.addEventListener('touchend', touchBuffer) } }
                doc.addEventListener(detectWheel(), setIntent, supportsPassive ? { passive: !0 } : !1); doc.addEventListener('keydown', updateInput)
            }; var updateInput = function updateInput(event) {
                if (!isBuffering) {
                    var eventKey = event.which; var value = inputMap[event.type]; if (value === 'pointer') value = pointerType(event); if (currentInput !== value || currentIntent !== value) {
                        var activeElem = document.activeElement; var activeInput = !1; var notFormInput = activeElem && activeElem.nodeName && formInputs.indexOf(activeElem.nodeName.toLowerCase()) === -1; if (notFormInput || changeIntentMap.indexOf(eventKey) !== -1) { activeInput = !0 }
                        if (value === 'touch' || value === 'mouse' || value === 'keyboard' && eventKey && activeInput && ignoreMap.indexOf(eventKey) === -1) { currentInput = currentIntent = value; setInput() }
                    }
                }
            }; var setInput = function setInput() {
                doc.setAttribute('data-whatinput', currentInput); doc.setAttribute('data-whatintent', currentInput); if (inputTypes.indexOf(currentInput) === -1) { inputTypes.push(currentInput); doc.className += ' whatinput-types-' + currentInput }
                fireFunctions('input')
            }; var setIntent = function setIntent(event) {
                if (mousePos.x !== event.screenX || mousePos.y !== event.screenY) { isScrolling = !1; mousePos.x = event.screenX; mousePos.y = event.screenY } else { isScrolling = !0 }
                if (!isBuffering && !isScrolling) { var value = inputMap[event.type]; if (value === 'pointer') value = pointerType(event); if (currentIntent !== value) { currentIntent = value; doc.setAttribute('data-whatintent', currentIntent); fireFunctions('intent') } }
            }; var touchBuffer = function touchBuffer(event) { if (event.type === 'touchstart') { isBuffering = !1; updateInput(event) } else { isBuffering = !0 } }; var fireFunctions = function fireFunctions(type) { for (var i = 0, len = functionList.length; i < len; i++) { if (functionList[i].type === type) { functionList[i].function.call(undefined, currentIntent) } } }; var pointerType = function pointerType(event) { if (typeof event.pointerType === 'number') { return pointerMap[event.pointerType] } else { return event.pointerType === 'pen' ? 'touch' : event.pointerType } }; var detectWheel = function detectWheel() {
                var wheelType = void 0; if ('onwheel' in document.createElement('div')) { wheelType = 'wheel' } else { wheelType = document.onmousewheel !== undefined ? 'mousewheel' : 'DOMMouseScroll' }
                return wheelType
            }; if ('addEventListener' in window && Array.prototype.indexOf) { setUp() }
            return { ask: function ask(opt) { return opt === 'loose' ? currentIntent : currentInput }, types: function types() { return inputTypes }, ignoreKeys: function ignoreKeys(arr) { ignoreMap = arr }, onChange: function onChange(funct, eventType) { functionList.push({ function: funct, type: eventType }) } }
        }();/***/
    })])
})