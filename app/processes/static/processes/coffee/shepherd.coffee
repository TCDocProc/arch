class window.ARCHShepherd
  init: ->
    unless $.cookie('seenTour')?
        if $(window).width() < 800
            $.cookie 'seenTour', true
            setTimeout @setupShepherd, 800

    $("#show_shepherd").click @setupShepherd

  setupShepherd: ->

    Backbone.history.navigate "/processes/", true

    @shepherd = new Shepherd.Tour
      defaults:
        classes: 'shepherd-element shepherd-open shepherd-theme-default'
        showCancelLink: true

    @shepherd.on 'cancel', ->
        $.mask.close()

    @shepherd.addStep 'step1',
      title: 'Hi There!'
      text: [
        'This is a little guide to show you how this system works.',
        'This system tells you more about what has, is and will happen in your healthcare journey.'
      ]
      attachTo:
        element: '.content > .branch > .sequence'
        on: 'bottom'
      classes: 'shepherd shepherd-open shepherd-theme-default shepherd-transparent-text'
      buttons: [
        text: 'Exit'
        classes: 'shepherd-button-secondary'
        action: @shepherd.cancel
      ,
        text: 'Next'
        action: @shepherd.next
        classes: 'shepherd-button-example-primary'
      ]
      when:
        show: ->
          $(".content > .branch > .sequence").expose
            closeOnClick: false
            closeOnEsc: false
            color: 'black'

    @shepherd.addStep 'step2',
      text: [
        'This box is what we call a “Pathway”. It’s a list showing all the steps in your treatment for a particular condition with the oldest at the top and the furthest in the future at the bottom.',
        'Click on this one to see the details.'
      ]
      attachTo:
        element: '.content > .branch > .sequence'
        on: 'bottom'
      classes: 'shepherd shepherd-open shepherd-theme-default shepherd-transparent-text'
      buttons: [
        text: 'Exit'
        classes: 'shepherd-button-secondary'
        action: @shepherd.cancel
      ,
        text: 'Next'
        action: @shepherd.next
        classes: 'shepherd-button-example-primary'
      ]
      when:
        'before-hide': ->
          if not $("#minimap :first-child").is(":visible")
            if $(".content > .branch > .sequence:nth-child(1)").length
              $(".content > .branch > .sequence:nth-child(1)").click()
      advanceOn:
        selector: '.content > .branch > .sequence *'
        event: 'click'

    @shepherd.addStep 'step3',
      title: 'The Steps in a Pathway'
      text: 'Each of these boxes represents a step in your treatment, click all the way into one to see the detail pop up. If steps are side by side, that means they can be done at the same time.'
      attachTo:
        element: '.content > .branch > .sequence'
        on: 'right'
      classes: 'shepherd shepherd-open shepherd-theme-default shepherd-transparent-text'
      buttons: [
        text: 'Exit'
        classes: 'shepherd-button-secondary'
        action: @shepherd.cancel
      ,
        text: 'Next'
        action: @shepherd.next
        classes: 'shepherd-button-example-primary'
      ]

    @shepherd.addStep 'step4',
      title: 'Your Colour Guide'
      text: 'This guide at the top left shows you what the colours of each of the steps mean, as you can see blue’s the most important as it shows you whats happening to you right now'
      attachTo:
        element: '.pushy-item:nth-child(3)'
        on: 'right'
      classes: 'shepherd shepherd-open shepherd-theme-default shepherd-transparent-text'
      buttons: [
        text: 'Exit'
        classes: 'shepherd-button-secondary'
        action: @shepherd.cancel
      ,
        text: 'Next'
        action: @shepherd.next
        classes: 'shepherd-button-example-primary'
      ]
      when:
        show: ->
          $.mask.close()
          setTimeout ->
              $(".pushy").expose
                closeOnClick: false
                closeOnEsc: false
                color: 'black'
          , 500

    @shepherd.addStep 'step5',
      title: 'Minimap and Going Home'
      text: [
        'As you can see this map shows where you are in any specific treatment pathway. No matter how deep you get you can always click this to go back to the top.'
        'You can also click "YourPathways" to go back home, try it!'
      ]
      attachTo:
        element: '#minimap'
        on: 'right'
      classes: 'shepherd shepherd-open shepherd-theme-default shepherd-transparent-text'
      buttons: [
        text: 'Exit'
        classes: 'shepherd-button-secondary'
        action: @shepherd.cancel
      ,
        text: 'Next'
        action: @shepherd.next
        classes: 'shepherd-button-example-primary'
      ]
      advanceOn: 'li.name click'

    @shepherd.addStep 'step6',
      title: 'Well Done!'
      text: [
        'You now have the power to fully understand your healthcare and know what’s happening to you at all times.'
        'If you see anything here that interests you, don’t be afraid to contact your healthcare professional and ask them for further information.'
        'Now go explore!'
      ]
      classes: 'shepherd shepherd-open shepherd-theme-default shepherd-transparent-text'
      buttons: [
        text: 'Done'
        action: @shepherd.next
        classes: 'shepherd-button-example-primary'
      ]
      when:
        show: ->
          $.mask.close()

    @shepherd.start()
