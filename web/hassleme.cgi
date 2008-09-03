#!/usr/bin/perl -w -I../perllib
#
# hassleme.cgi:
# Website for hassleme.
#
# Copyright (c) 2005 Chris Lightfoot. All rights reserved.
# Email: chris@ex-parrot.com; WWW: http://www.ex-parrot.com/~chris/
#

my $rcsid = ''; $rcsid .= '$Id: hassleme.cgi,v 1.1 2008-09-03 15:36:28 francis Exp $';

use strict;

use CGI qw(-no_xhtml);
use CGI::Fast;
use Data::Dumper;
use HTML::Entities qw(encode_entities);
use IO::Pipe;
use HTML::Entities;
use Net::DNS;

use Hassle;
use Hassle::Config;

sub _ {
    # TODO - this is the function that will become the stub function for il18n and l10n
    return @_;
}

sub hassle_header {
    my ($q, $title) = @_;
    my $fn = lc($q->param('fn'));
    $fn ||= 'home';
    my $header_title = "HassleMe";
    if ($title) {
        $header_title .= " - $title";
    }
    print
        $q->header(-type => 'text/html; charset=utf-8'),
        $q->start_html(-title=>$header_title,
                       -style=>{-src=>'/hassleme.css'},
#                       -script=>{-language=>'JAVASCRIPT',
#                                 -src=>'yellowFade.js'}
                       );
    print $q->h1($q->a({href=>'/'},"HassleMe"),
#                 $q->span({-id=>'betaTest'},
#                        'Beta Test'),
                 $q->span({-id=>'slogan'},
                          _("Because sometimes in life,<br/>you just need to be nagged...")),
                 );
    print _('<div id="w"><div id="content">');
    if ($title) {
        print $q->h2($title);
    }
}

sub hassle_intro {
    print <<EOF;
<div id="intro">
<p>Not eating enough fruit? Forgot to feed the fish again? Need a little help keeping your New Year's resolutions?
<br/>
<b>Tell us what to hassle you about, and we'll nag you via email at semi-unpredictable intervals.</b></p>
</div>
EOF
}

sub hassle_form {
    my ($q) = @_;

    $q->delete('fn');

    print $q->div({id=>'createHassleBox'},
              $q->start_form(-name => 'createHassleForm',
                             -action => '/',    # XXX
                             -method => 'POST',
                             -enctype => 'application/x-www-form-urlencoded',
                             -accept_charset => 'UTF-8'),
              $q->hidden(-name => 'fn',
                         -value => 'home'),
              $q->hidden(-name => 'f'),
              $q->h2('Set up a hassle now!'),
              $q->p(
                    'Hassle me roughly every ',
                    $q->textfield(-name => 'freq', -size => 3),
#                    $q->popup_menu(-name => 'units',
#                                   -values => ['days','hours','minutes']),
#                        $q->br(),
#                    ', reminding me to:',
                    'days, reminding me to:',
                    $q->textarea(
                                 -style => 'width: 25em;',
                                 -name => 'what', -cols => 25, -rows => 3),
                    ),
              $q->p(
                    'Send the emails to: ',
                    $q->textfield(-name => 'email', -size => 25),
                    ),
              $q->ul(
                    $q->li("We'll send you a confirmation email when you sign up."),
                    $q->li("If you add more than one email address (separated by commas or semicolons) we'll pick one person at random for each hassle &mdash; good for offices!"),
                    ),
              $q->p(
                    'Can we make the text of this hassle publicly visible?',
                    $q->br(),
                    $q->radio_group(-name=>'public',
                                    -values=>['true','false'],
                                    -default=>'false',
                                    -labels=>{'true'=>'Yes','false'=>'No'}),
                    ),
              $q->submit(-value => 'Set up this hassle now >>'),
              $q->end_form(),
              );

    hassle_recent($q);
}

sub hassle_recent {
    my ($q) = @_;

        print <<EOF;
<div id="exampleHasslesBox">
<h2>Popular Hassles</h2>
<ul>
<li><b>Go to the gym</b> roughly every 4 days</li>
<li><b>Write an entry in my diary</b> roughly every 3 days</li>
<li><b>Call your mother</b> roughly every 7 days</li>
<li><b>Go to the theatre</b> roughly every 21 days</li>
<li><b>Spend 5 hours doing something for <a href="http://www.mysociety.org/volunteertasks">mySociety</a></b> roughly every 28 days</li>
<li><b>Practice the piano</b> roughly every 3 days</li>
<li><b>Go for a walk in the park</b> roughly every 10 days</li>
</ul>
<!--
<h2>Recently on HassleMe</h2>
<ul>People asked to be sent these hassles:
<li><a href="/hassleme.cgi?fn=home&f=1&freq=14&what=Go+to+the+theatre&public=false&email=">Go to the theatre every 14 days</a></li>
<li><a href="/hassleme.cgi?fn=home&f=1&freq=4&what=Go+to+the+gym&public=false&email=">Go to the gym every 4 days</a></li>
<li><a href="/hassleme.cgi?fn=home&f=1&freq=7&what=Call+your+mother&public=false&email=">Call your mother every 7 days</a></li>
</ul>
-->
</div>

<div id="news">
<h2>Upcoming Features</h2>
<ul>
<li>Get hassled via <acronym title="Instant Messaging services like AIM, ICQ, MSN Messenger, Jabber, Google Talk">IM</acronym>.</li>
<li>Specify time in hours, days, weeks and months.</li>
<li>Translation into other languages.</li>
<li>Other cool stuff!</li>
</ul>
</div>

EOF

}

sub hassle_footer {
    my ($q) = @_;
    print <<EOF,

</div></div>

<p id="footer">
<a href="http://digg.com/software/HassleMe_nags_you_because_your_mother_can_t_do_everything">Digg this!</a> |
<a href="/faq">FAQ</a> |
Derived from <a href="http://www.mysociety.org/?p=16">Hasslebot</a>, a
<a href="http://www.mysociety.org/">mySociety</a> tool that reminds us to post
things on our <a href="http://www.mysociety.org/?cat=2">blog</a><br />
Hosted and supported by
<a href="http://www.mythic-beasts.com/">Mythic Beasts Ltd</a>
</p>

EOF
        $q->end_html();
}

my $foad = 0;
$SIG{TERM} = sub { $foad = 1; };
while (!$foad && (my $q = new CGI::Fast())) {
#    $q->autoEscape(0);
    my $fn = lc($q->param('fn'));
    $fn ||= 'home';
    my %fns = map { $_ => 1 } qw(home confirm unsubscribe faq);
    $fn = 'home' if (!exists($fns{$fn}));

    my $created = undef;

    if ($fn eq 'home') {
        my $emails = $q->param('email');
        my $freq = $q->param('freq');
        my $units = $q->param('units');
        my $what = $q->param('what');
        my $public = lc($q->param('public'));

        my @errors = ( );

        if ($q->param('f')) {
            if (!defined($freq) || $freq eq '') {
                push(@errors, "Please tell us how often you want to be hassled");
            } elsif ($freq !~ /^[1-9]\d*$/) {
                push(@errors, "Number of days should be a number, like '7'");
            } elsif ($freq > 3650) {
                push(@errors, "Surely you want to be hassled more than once every ten years?");
            }

            if (defined($public)) {
                if ($public ne 'true' && $public ne 'false') {
                    push(@errors, "Marking a hassle publicly visible should be either 'true' or 'false'.");
                }
            } else {
                $public = 'false';
            }

            if (!defined($what) || $what =~ /^\s*$/) {
                push(@errors, 'Please tell us what you want to be hassled about');
            }

#            if (!defined($units) || $units eq '') {
#                push(@errors, "Please select hours or days");
#            } elsif ($units !~ /(days|hours)/) {
#                push(@errors, "Sorry, you can only specify hours or days");
#            }

            my @emails;
            if (!$emails) {
                push(@errors, "Please enter an email address or addresses");
            } else {
                $emails =~ s/\s//mg;
                my %e;
                @emails = grep { ++$e{$_}; $e{$_} == 1 } split('[,;]', $emails);
                push(@errors, grep { defined($_) } map { Hassle::is_valid_email($_) } @emails);
            }

            if (!@errors) {
                # Actually create it.
                my $hassle_id = dbh()->selectrow_array("select nextval('hassle_id_seq')");

                # TODO - funky arithmetic to modify the frequency
                # depending on unit of time used (days = no change,
                # hours, weeks, etc = change).

                # strip out newlines in $what or emails get borked Subject: lines

                $what =~ s/[\r\n]+/ /g;

                # remove the capacity for spammers to put vast
                # quantities of text in a hassle

                my $what_preview = $what;
                my $preview_length = 512;
                if (length($what) > $preview_length) {
                    $what_preview = substr($what_preview, 0, $preview_length - 3) . '...';
                }
                
                my $t0 = time();
                dbh()->do('
                        insert into hassle (id, frequency, what, public, ipaddr)
                        values (?, ?, ?, ?, ?)', {},
                        $hassle_id, $freq, $what, $public, $q->remote_host());

                my @printable_emails = map { encode_entities($_) } @emails;
                foreach my $email (@emails) {
                    my $recipient_id = dbh()->selectrow_array("select nextval('recipient_id_seq')");
                    dbh()->do('
                              insert into recipient (id, hassle_id, email)
                              values (?, ?, ?)', {},
                              $recipient_id, $hassle_id, $email);
                    dbh()->commit();

                    my $confirmurl = mySociety::Config::get('WEBURL') . "/C/" . token($recipient_id);

                    my $t1 = time();
                    sendmail($email, "Please confirm you want to be hassled to \"$what_preview\"",
                             <<EOF,

Hello,

Someone (hopefully you) has asked for this email address to be hassled
roughly every $freq days to:

$what_preview

If you want to be hassled about this, please click on the link below:
    $confirmurl

If your email program does not let you click on this link, just copy
and paste it into your web browser and hit return.

If you have changed your mind and don't want us to nag you, then do
nothing - your message will expire and be deleted.

Any other questions? Please email team\@hassleme.co.uk and we'll get
back to you as soon as we can.

Thanks!

--The HassleMe Team

EOF
                            );
                    my $dt = time() - $t1;
                    warn "sending email to <$email> about hassle #$hassle_id took ${dt}s"
                        if ($dt > 30);
                }

                my $dt = time() - $t0;
                warn "creating hassle #$hassle_id took ${dt}s"
                    if ($dt > 30);

                $q->delete('what','freq','public');

                $created = 1;
                my $printable_emails = join(', ',@printable_emails);

                my $singular_or_plural = (@printable_emails == 1
                                          ? 'a confirmation email'
                                          : 'confirmation emails');

                hassle_header($q,'Thanks!');
                print $q->div({-id=>'message'},
                            $q->ul(
                                   $q->li("We've sent $singular_or_plural to <em>$printable_emails</em>; you'll need to click on the link in the email before we can hassle you."),
                                   $q->li("If you're using <acronym title='Web-based email systems like Oddpost, Gmail, MSN Hotmail, or Yahoo! Mail'>webmail</acronym>, you might want to check your <em>Spam</em>, <em>Junk</em> or <em>Bulk Mail</em> folders."),
                                   $q->li("<strong>Since you're here, why not set up another hassle (or two)?</strong>")));
            }
        } else {
            hassle_header($q);
        }

        $q->param('f', 1);
    
        if (@errors) {
            hassle_header($q);
            print $q->h3("Sorry, that didn't work."),
                  $q->ul({-id=>'errors'},
                    $q->li([
                            map { encode_entities($_) } @errors
                        ])
                    );
        }
        unless ($created || @errors) {
            hassle_intro();
        }

        hassle_form($q);

    } elsif ($fn eq 'confirm') {
        my $token = $q->param('token');
        my $id = check_token($token);
        if (defined($id)) {
            dbh()->do('update recipient set confirmed = true where id = ?',
                        {}, $id);
            dbh()->commit();
            hassle_header($q,'Confirmed!');
            print <<EOF;
<div id="message">
<p>
<b>Thanks &mdash; prepare to be hassled!</b>
</p><p>
Have you heard about our sister sites <a href="http://HearFromYourMP.com">HearFromYourMP.com</a> (if you are in
the UK) or <a href="http://PledgeBank.com">PledgeBank.com</a> (if you are anywhere in the world, including
the UK?) They're what <a href="http://www.mysociety.org/">mySociety</a> is really all about &mdash; have a go now!
</p><p>
We're always seeking volunteers to help build and publicise sites like
these &mdash; <a href="http://www.mysociety.org/volunteertasks.cgi">why not get involved</a>?
</p>
</div>
EOF
        } else {
                hassle_header($q,'Oops!');
                print $q->p({-id=>'errors'},
                            "Sorry. We couldn't understand the link you've followed."
                            );
            }
        hassle_form($q);
    } elsif ($fn eq 'unsubscribe') {
        my $token = $q->param('token');
        my $id = check_token($token);
        if (defined($id)) {
            dbh()->do('delete from recipient where id = ?',
                        {}, $id);
            dbh()->commit();
            hassle_header($q,'Stopped!');
            print $q->p({-id=>'message'},
                    "Thanks! We'll stop hassling you about that, starting now."
                );
        } else {
            hassle_header($q,'Oops!');
            print $q->p({-id=>'errors'},
                    "Sorry. We couldn't understand the link you've followed."
                );
        }
        hassle_form($q);
    } elsif ($fn eq 'faq') {
                hassle_header($q,'Frequently Asked Questions');
                print <<EOF;
<dl>

<dt>Something's not working &mdash; who do I tell?</dt>

<dd>Please email <a
href="mailto:etienne\@mysociety.org">etienne\@mysociety.org</a> with a
short description of what page you were on; what <em>should</em> have
happened; what <em>actually</em> happened; and roughly what time the
error occured. Thanks!</dd>

<dt>What is this site?</dt>

<dd>HassleMe is a tool which nags you. It nags you via email about things
you know you should be doing, but which you'll forget.</dd>

<dt>How often does it nag?</dt>

<dd>You set up a rough frequency, but it actually nags you at random times
within certain parameters. It keeps you on your toes.</dd>

<dt>Why do you think it'll work?</dt>

<dd>mySociety's developer <a href="http://www.ex-parrot.com/~chris/">Chris
Lightfoot</a> built a little program called
<a href="http://www.mysociety.org/?p=16">Hasslebot</a>, to encourage the
developers and volunteers at mySociety to post frequently to our blog, letting
people know what mySociety was up to. Despite the fact that it shouldn't work,
it did.</dd>

<dt>If I give you my email address, will you send me spam?<dt>

<dd><b>No!</b> We will only ever send you email when someone
(hopefully you) uses this website to set up a hassle (i.e. we'll send
you a "please confirm this hassle" email), and to carry out the actual
hassling (i.e. the regular nagging emails telling you to go the gym,
write to your mother, etc.). We won't sell your email address to
anyone, and we won't send you spam &mdash; ever.</dd>

<dt>Who are you?</dt>

<dd>This site was built by <a
href="http://www.ex-parrot.com/~chris/">Chris Lightfoot</a> and <a
href="http://ejhp.net/">Etienne Pollard</a> in two afternoons before
and after Christmas 2005 as a mySociety 'back of the envelope'
project. Chris is a full-time employee of mySociety and spends his
days running much more serious sites like <a
href="http://www.writetothem.com/">WriteToThem.com</a>. <a
href="http://www.mysociety.org/">mySociety</a> is a charitable
organisation which has grown out of the community of volunteers who
built sites like <a
href="http://www.theyworkforyou.com/">TheyWorkForYou.com</a>. Our
primary mission is to build internet projects which give people
simple, tangible benefits in the civic and community aspects of their
lives. Our first project was <a
href="http://www.writetothem.com/">WriteToThem.com</a>, where you can
write to any of your elected representatives, for free, and our more
recent sites include <a
href="http://www.pledgebank.com/">PledgeBank.com</a> and <a
href="http://www.placeopedia.com/">Placeopedia.com</a>.</dd>

EOF

    }
    hassle_footer($q);
}
