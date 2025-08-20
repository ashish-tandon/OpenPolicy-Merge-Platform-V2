'use client';

import { Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { XMarkIcon } from '@heroicons/react/24/outline';
import { useAccessibility } from './AccessibilityProvider';

interface AccessibilitySettingsProps {
  isOpen: boolean;
  onClose: () => void;
}

/**
 * Accessibility settings panel
 * Allows users to customize their viewing experience
 */
export default function AccessibilitySettings({ isOpen, onClose }: AccessibilitySettingsProps) {
  const { fontSize, setFontSize, reducedMotion, highContrast } = useAccessibility();
  
  return (
    <Transition.Root show={isOpen} as={Fragment}>
      <Dialog as="div" className="relative z-50" onClose={onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex min-h-full items-center justify-center p-4 text-center sm:p-0">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
              enterTo="opacity-100 translate-y-0 sm:scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 translate-y-0 sm:scale-100"
              leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            >
              <Dialog.Panel className="relative transform overflow-hidden rounded-lg bg-white px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
                <div className="absolute right-0 top-0 pr-4 pt-4">
                  <button
                    type="button"
                    className="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    onClick={onClose}
                  >
                    <span className="sr-only">Close</span>
                    <XMarkIcon className="h-6 w-6" aria-hidden="true" />
                  </button>
                </div>
                
                <div className="sm:flex sm:items-start">
                  <div className="mt-3 text-center sm:mt-0 sm:text-left w-full">
                    <Dialog.Title as="h3" className="text-lg font-semibold leading-6 text-gray-900">
                      Accessibility Settings
                    </Dialog.Title>
                    
                    <div className="mt-6 space-y-6">
                      {/* Font Size */}
                      <div>
                        <label className="text-sm font-medium text-gray-700">
                          Text Size
                        </label>
                        <div className="mt-2 space-y-2">
                          <label className="flex items-center">
                            <input
                              type="radio"
                              name="fontSize"
                              value="normal"
                              checked={fontSize === 'normal'}
                              onChange={() => setFontSize('normal')}
                              className="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-600"
                            />
                            <span className="ml-3 text-sm">Normal</span>
                          </label>
                          <label className="flex items-center">
                            <input
                              type="radio"
                              name="fontSize"
                              value="large"
                              checked={fontSize === 'large'}
                              onChange={() => setFontSize('large')}
                              className="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-600"
                            />
                            <span className="ml-3 text-sm">Large</span>
                          </label>
                          <label className="flex items-center">
                            <input
                              type="radio"
                              name="fontSize"
                              value="extra-large"
                              checked={fontSize === 'extra-large'}
                              onChange={() => setFontSize('extra-large')}
                              className="h-4 w-4 border-gray-300 text-indigo-600 focus:ring-indigo-600"
                            />
                            <span className="ml-3 text-sm">Extra Large</span>
                          </label>
                        </div>
                      </div>
                      
                      {/* System Preferences Info */}
                      <div className="rounded-md bg-blue-50 p-4">
                        <div className="flex">
                          <div className="ml-3">
                            <h4 className="text-sm font-medium text-blue-800">
                              System Preferences Detected
                            </h4>
                            <div className="mt-2 text-sm text-blue-700">
                              <ul className="list-disc space-y-1 pl-5">
                                {reducedMotion && (
                                  <li>Reduced motion is enabled</li>
                                )}
                                {highContrast && (
                                  <li>High contrast mode is active</li>
                                )}
                                {!reducedMotion && !highContrast && (
                                  <li>No special preferences detected</li>
                                )}
                              </ul>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      {/* Keyboard Shortcuts */}
                      <div>
                        <h4 className="text-sm font-medium text-gray-700 mb-2">
                          Keyboard Shortcuts
                        </h4>
                        <dl className="space-y-1 text-sm text-gray-600">
                          <div className="flex justify-between">
                            <dt>Skip to main content</dt>
                            <dd className="font-mono">Tab (at page start)</dd>
                          </div>
                          <div className="flex justify-between">
                            <dt>Navigate menu</dt>
                            <dd className="font-mono">Arrow keys</dd>
                          </div>
                          <div className="flex justify-between">
                            <dt>Close dialogs</dt>
                            <dd className="font-mono">Esc</dd>
                          </div>
                          <div className="flex justify-between">
                            <dt>Submit forms</dt>
                            <dd className="font-mono">Enter</dd>
                          </div>
                        </dl>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="mt-6 sm:flex sm:flex-row-reverse">
                  <button
                    type="button"
                    className="inline-flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 sm:ml-3 sm:w-auto"
                    onClick={onClose}
                  >
                    Done
                  </button>
                </div>
              </Dialog.Panel>
            </Transition.Child>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
}
