;; -*- mode: emacs-lisp -*-
;; This file is loaded by Spacemacs at startup.
;; It must be stored in the home directory.

;; Variables

(defvar dotspacemacs-configuration-layers '(syl20bnr)
  "list of contribution to load."
)

(defvar dotspacemacs-default-package-repository 'melpa-stable
  "The default package repository used if no explicit repository has been
specified with an installed package."
)

;; Functions

(defun dotspacemacs/init ()
  "User initialize for Spacemacs. This function is called at the very startup."
  (defvar spacemacs-normal-state-sequence '(?f . ?d))
  (defvar spacemacs-normal-state-sequence-delay 0.1))

(defun dotspacemacs/config ()
  "This is were you can ultimately override default Spacemacs configuration.
This function is called at the very end of Spacemacs initialization."
  ;; switch meta for super in order to play nicely with i3wm which I use with
  ;; alt modifier.
  (setq x-super-keysym 'meta)
  (setq x-meta-keysym 'super)
  ;; I prefer to stay on the original character when leaving insert mode
  ;; (initiated with 'i').
  (setq evil-move-cursor-back nil))
